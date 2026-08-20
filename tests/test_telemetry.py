from __future__ import annotations

import copy
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
            "description", "homepageUrl", "name", "nameWithOwner", "object",
            "owner", "primaryLanguage", "repository", "resourcePath",
            "sshUrl", "topics", "url",
        }
        for field in forbidden:
            self.assertIsNone(
                re.search(rf"\b{re.escape(field)}\b", PRIVATE_SAFE_QUERY),
                msg=f"query must not request identifying field {field}",
            )
        self.assertIn("restrictedContributionsCount", PRIVATE_SAFE_QUERY)
        self.assertIn("pageInfo", PRIVATE_SAFE_QUERY)
        self.assertIn("stargazerCount", PRIVATE_SAFE_QUERY)

    def test_public_count_is_fork_inclusive_and_stars_are_nonfork_paginated(self) -> None:
        self.assertRegex(
            PRIVATE_SAFE_QUERY,
            r"publicRepositories:\s*repositories\([^)]*privacy:\s*PUBLIC[^)]*\)",
        )
        public_selection = re.search(
            r"publicRepositories:\s*repositories\(([^)]*)\)", PRIVATE_SAFE_QUERY
        )
        star_selection = re.search(
            r"starredRepositories:\s*repositories\(([^)]*)\)", PRIVATE_SAFE_QUERY
        )
        self.assertIsNotNone(public_selection)
        self.assertIsNotNone(star_selection)
        self.assertNotIn("isFork", public_selection.group(1))
        self.assertIn("isFork: false", star_selection.group(1))
        self.assertIn("after: $cursor", star_selection.group(1))

    def test_parser_discards_unexpected_sensitive_identifiers(self) -> None:
        stats = parse_stats(json.loads(FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(stats.contributions_ytd, 742)
        self.assertEqual(stats.private_contributions_ytd, 311)
        self.assertEqual(stats.merged_pull_requests, 97)
        self.assertEqual(stats.public_repositories, 4)
        self.assertEqual(stats.repositories_contributed_to, 18)
        self.assertEqual(stats.stars_earned, 21)
        self.assertNotIn("SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE", repr(stats))

    def test_fetch_paginates_star_counts_without_requesting_repo_identity(self) -> None:
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
            payload = copy.deepcopy(fixture)
            page = payload["data"]["user"]["starredRepositories"]
            payload["data"]["user"]["publicRepositories"]["totalCount"] = 101
            if variables["cursor"] is None:
                page["nodes"] = [{"stargazerCount": 5}]
                page["pageInfo"] = {"hasNextPage": True, "endCursor": "page-2"}
            else:
                page["nodes"] = [
                    {"stargazerCount": 7},
                    {"stargazerCount": 11},
                ]
                page["pageInfo"] = {"hasNextPage": False, "endCursor": None}
            return payload

        stats = fetch_stats(
            token="token",
            now=datetime(2026, 8, 21, 12, tzinfo=timezone.utc),
            timeout_seconds=3.0,
            transport=transport,
        )

        self.assertEqual(stats.public_repositories, 101)
        self.assertEqual(stats.stars_earned, 23)
        self.assertEqual([call["cursor"] for call in calls], [None, "page-2"])
        self.assertEqual(calls[0]["from"], "2026-01-01T00:00:00Z")
        self.assertEqual(calls[0]["to"], "2026-08-21T12:00:00Z")

    def test_parser_rejects_graphql_errors(self) -> None:
        with self.assertRaisesRegex(ValueError, "GitHub GraphQL"):
            parse_stats({"errors": [{"message": "denied"}]})


if __name__ == "__main__":
    unittest.main()
