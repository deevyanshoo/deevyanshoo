from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from operator_profile.model import GitHubStats, ProfileData
from operator_profile.render import render_profile


class DeterministicRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = ProfileData(
            stats=GitHubStats(
                contributions_ytd=742,
                private_contributions_ytd=311,
                commit_contributions_ytd=526,
                pull_request_contributions_ytd=84,
                issue_contributions_ytd=19,
                review_contributions_ytd=113,
                merged_pull_requests=97,
                public_repositories=4,
                repositories_contributed_to=18,
                stars_earned=21,
            )
        )

    def test_same_input_produces_byte_identical_svg(self) -> None:
        self.assertEqual(
            render_profile(self.data, "dark").encode(),
            render_profile(self.data, "dark").encode(),
        )

    def test_both_themes_are_valid_and_distinct(self) -> None:
        light = render_profile(self.data, "light")
        dark = render_profile(self.data, "dark")
        ET.fromstring(light)
        ET.fromstring(dark)
        self.assertIn('data-theme="light"', light)
        self.assertIn('data-theme="dark"', dark)
        self.assertNotEqual(light, dark)

    def test_output_contains_story_and_capability_neutral_privacy_label(self) -> None:
        svg = render_profile(self.data, "dark")
        for phrase in (
            "DEEVYANSHOO // OPERATOR", "making large models fit small boxes",
            "Nnomi", "Chauffit", "runtime", "v26", "garage_target", "911",
            "RECENT REPOS", "PRIVACY MODE", "AGGREGATE ONLY",
        ):
            self.assertIn(phrase, svg)
        self.assertNotIn("PRIVATE ACTIVITY", svg)
        self.assertNotIn("SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE", svg)

    def test_renderer_escapes_dynamic_text(self) -> None:
        svg = render_profile(self.data, "dark", status_label="A&B <ready>")
        self.assertIn("A&amp;B &lt;ready&gt;", svg)
        ET.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
