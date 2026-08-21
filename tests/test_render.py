from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from operator_profile.model import GitHubStats, ProfileData
from operator_profile.render import render_profile, render_systems


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
        self.assertEqual(
            render_systems("dark").encode(),
            render_systems("dark").encode(),
        )

    def test_both_themes_are_valid_and_distinct(self) -> None:
        light = render_profile(self.data, "light")
        dark = render_profile(self.data, "dark")
        systems_light = render_systems("light")
        systems_dark = render_systems("dark")
        for svg in (light, dark, systems_light, systems_dark):
            ET.fromstring(svg)
        self.assertIn('data-theme="light"', light)
        self.assertIn('data-theme="dark"', dark)
        self.assertNotEqual(light, dark)
        self.assertNotEqual(systems_light, systems_dark)

    def test_profile_has_identity_hierarchy_without_vanity_metrics(self) -> None:
        svg = render_profile(self.data, "dark")
        for phrase in (
            "deevyanshoo@operator",
            "making large models fit small boxes",
            "CURRENT MISSION // NNOMI",
            "NNOMI",
            "CHAUFFIT",
            "runtime v26",
            "garage_target 911",
            "742 CONTRIBUTIONS YTD",
        ):
            self.assertIn(phrase, svg)

        for unwanted in (
            "MERGED PRS",
            "STARS EARNED",
            "PUBLIC REPOS",
            "RECENT REPOS",
            "PRIVACY MODE",
            "SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE",
        ):
            self.assertNotIn(unwanted, svg)

    def test_systems_panel_tells_engineering_story(self) -> None:
        svg = render_systems("dark")
        for phrase in (
            "THINGS I BUILT BECAUSE I COULD",
            "JARVIS",
            "HYBRID AI",
            "DAG LEDGER",
            "DISTRIBUTED SYSTEMS",
            "AVIATION",
            "FORECASTING AT SCALE",
            "&gt;90%",
            "~800 TB/day",
        ):
            self.assertIn(phrase, svg)

    def test_renderer_escapes_dynamic_text(self) -> None:
        svg = render_profile(self.data, "dark", status_label="A&B <ready>")
        self.assertIn("A&amp;B &lt;ready&gt;", svg)
        ET.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
