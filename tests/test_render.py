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

    def test_profile_has_identity_hierarchy_and_personality(self) -> None:
        svg = render_profile(self.data, "dark")
        required = (
            "deevyanshoo@operator",
            "making large models fit small boxes",
            "CURRENT MISSION // NNOMI",
            "NNOMI",
            "CHAUFFIT",
            "AI-powered, safety-first on-demand driver marketplace",
            "Gurugram ↔ wherever",
            "MSE DATA SCIENCE // UPENN",
            "AI ARCHITECT @ ZS",
            "coffee ........ required",
            "runtime ........ v26",
            "inference ..... local &gt; cloud",
            "garage_target .. 911",
            "742 CONTRIBUTIONS YTD",
        )
        for phrase in required:
            self.assertIn(phrase, svg)

        forbidden = (
            "MERGED PRS",
            "STARS EARNED",
            "PUBLIC REPOS",
            "RECENT REPOS",
            "PRIVACY MODE",
            "approved portrait",
            "approved desk portrait",
            "image-derived",
            "SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, svg)

    def test_systems_panel_tells_engineering_story(self) -> None:
        svg = render_systems("dark")
        for phrase in (
            "THINGS I BUILT BECAUSE I COULD",
            "JARVIS",
            "personal JARVIS on a phone",
            "HYBRID AI",
            "DAG LEDGER",
            "DISTRIBUTED SYSTEMS",
            "AVIATION",
            "FORECASTING AT SCALE",
            "&gt;90%",
            "~800 TB/day",
            "not demos // systems that had to work",
        ):
            self.assertIn(phrase, svg)

    def test_renderer_escapes_dynamic_text(self) -> None:
        svg = render_profile(self.data, "dark", status_label="A&B <ready>")
        self.assertIn("A&amp;B &lt;ready&gt;", svg)
        ET.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
