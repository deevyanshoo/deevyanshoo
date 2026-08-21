from __future__ import annotations

import json
import re
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from operator_profile.telemetry import PRIVATE_SAFE_QUERY, fetch_stats, parse_stats


FIXTURE = Path(__file__).parent / "fixtures" / "github_response.json"


class TelemetryPrivacyTests(unittest.TestCase):
    def test_query_requests_only_aggregate_safe_fields(self) -> None:
        forbidden = {
            "branch", "commit", "description", "file", "homepageUrl", "issue",
            "name", "nameWithOwner", "nodes", "object", "organization", "owner",
            "primaryLanguage", "pullRequests", "repositories", "repository",
            "resourcePath", "sshUrl", "topics", "url",
        }
        for field in forbidden:
            self.assertIsNone(
                re.search(rf"\b{re.escape(field)}\b", PRIVATE_SAFE_QUERY),
                msg=f"query must not request identifying field {field}",
            )
        self.assertIn("restrictedContributionsCount", PRIVATE_SAFE_QUERY)
        self.assertIn("totalContributions", PRIVATE_SAFE_QUERY)

    def test_query_has_no_pagination_or_per_repository_selection(self) -> None:
        self.assertNotIn("$cursor", PRIVATE_SAFE_QUERY)
        self.assertNotIn("pageInfo", PRIVATE_SAFE_QUERY)
        self.assertNotIn("stargazerCount", PRIVATE_SAFE_QUERY)

    def test_parser_discards_unexpected_sensitive_identifiers(self) -> None:
        stats = parse_stats(json.loads(FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(stats.contributions_ytd, 742)
        self.assertEqual(stats.restricted_contributions_ytd, 311)
        self.assertNotIn("SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE", repr(stats))

    def test_fetch_requests_one_year_to_date_aggregate(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        calls: list[Mapping[str, Any]] = []

        def transport(
            token: str,
            variables: Mapping[str, Any],
            timeout_seconds: float,
        ) -> Mapping[str, Any]:
            self.assertEqual(token, "token")
            self.assertEqual(timeout_seconds, 3.0)
            calls.append(dict(variables))
            return fixture

        stats = fetch_stats(
            token="token",
            now=datetime(2026, 8, 21, 12, tzinfo=timezone.utc),
            timeout_seconds=3.0,
            transport=transport,
        )

        self.assertEqual(stats.contributions_ytd, 742)
        self.assertEqual(len(calls), 1)
        self.assertNotIn("cursor", calls[0])
        self.assertEqual(calls[0]["from"], "2026-01-01T00:00:00Z")
        self.assertEqual(calls[0]["to"], "2026-08-21T12:00:00Z")

    def test_parser_rejects_graphql_errors(self) -> None:
        with self.assertRaisesRegex(ValueError, "GitHub GraphQL"):
            parse_stats({"errors": [{"message": "denied"}]})


if __name__ == "__main__":
    unittest.main()
