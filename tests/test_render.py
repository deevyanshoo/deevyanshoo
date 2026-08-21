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
            "DIVYANSHU GOYAL",
            "AI ARCHITECT · FOUNDER · BUILDER",
            "making large models fit small boxes",
            "NNOMI",
            "India-first financial coach",
            "EARN",
            "SEE CLEARLY",
            "PROTECT",
            "INVEST",
            "BUILD WEALTH",
            "Gurugram ↔ wherever",
            "UNIVERSITY OF PENNSYLVANIA",
            "AI ARCHITECT @ ZS",
            "coffee ........ required",
            "runtime ........ v26",
            "inference ..... local &gt; cloud",
            "garage_target .. 911",
        )
        for phrase in required:
            self.assertIn(phrase, svg)

        forbidden = (
            "IDENTITY //",
            "PORTRAIT //",
            "CURRENT MISSION //",
            "CHAUFFIT",
            "MERGED PRS",
            "STARS EARNED",
            "PUBLIC REPOS",
            "RECENT REPOS",
            "PRIVACY MODE",
            "approved portrait",
            "approved desk portrait",
            "image-derived",
            "source portrait",
            "privacy mode",
            "SENSITIVE_SENTINEL_SHOULD_NOT_SURVIVE",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, svg)
        self.assertRegex(svg, r'class="sans mission-name"[^>]*>NNOMI</text>')

    def test_systems_panel_tells_engineering_story(self) -> None:
        svg = render_systems("dark")
        for phrase in (
            "THINGS I BUILT BECAUSE I COULD",
            "DAG LEDGER",
            "crawler / network logic",
            "peer approvals + validation incentives",
            "65 days ahead",
            "&gt;90% accuracy",
            "~800 TB/day",
            "JARVIS",
            "mobile-first personal AI",
            "quantized local SLM",
            "cloud LLM",
            "privacy · latency · capability",
        ):
            self.assertIn(phrase, svg)
        self.assertNotIn("HYBRID AI", svg)
        self.assertLess(svg.index("DAG LEDGER"), svg.index("AVIATION FORECASTING"))
        self.assertLess(svg.index("AVIATION FORECASTING"), svg.index("JARVIS"))

    def test_renderer_escapes_dynamic_text(self) -> None:
        svg = render_profile(self.data, "dark", status_label="A&B <ready>")
        self.assertIn("A&amp;B &lt;ready&gt;", svg)
        ET.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
