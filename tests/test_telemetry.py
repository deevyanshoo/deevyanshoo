from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from operator_profile.telemetry import PRIVATE_SAFE_QUERY, parse_stats


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
        self.assertIn("stargazerCount", PRIVATE_SAFE_QUERY)

    def test_parser_discards_unexpected_private_identifiers(self) -> None:
        stats = parse_stats(json.loads(FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(stats.contributions_ytd, 742)
        self.assertEqual(stats.private_contributions_ytd, 311)
        self.assertEqual(stats.merged_pull_requests, 97)
        self.assertEqual(stats.public_repositories, 4)
        self.assertEqual(stats.repositories_contributed_to, 18)
        self.assertEqual(stats.stars_earned, 21)
        self.assertNotIn("customer-zero-stealth-repo", repr(stats))

    def test_parser_rejects_graphql_errors(self) -> None:
        with self.assertRaisesRegex(ValueError, "GitHub GraphQL"):
            parse_stats({"errors": [{"message": "denied"}]})


if __name__ == "__main__":
    unittest.main()
