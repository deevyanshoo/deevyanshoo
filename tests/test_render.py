from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from operator_profile.model import GitHubStats, ProfileData
from operator_profile.render import render_profile, render_systems


class DeterministicRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = ProfileData(stats=GitHubStats(742, 311))

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
            "AI ARCHITECT \u00b7 FOUNDER \u00b7 BUILDER",
            "making large models fit small boxes",
            "NNOMI",
            "India-first financial coach",
            "EARN",
            "SEE CLEARLY",
            "PROTECT",
            "INVEST",
            "BUILD WEALTH",
            "Gurugram \u2194 wherever",
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
            "privacy \u00b7 latency \u00b7 capability",
        ):
            self.assertIn(phrase, svg)
        self.assertNotIn("HYBRID AI", svg)
        self.assertLess(svg.index("DAG LEDGER"), svg.index("AVIATION FORECASTING"))
        self.assertLess(svg.index("AVIATION FORECASTING"), svg.index("JARVIS"))

    def test_systems_geometry_is_asymmetric_and_in_bounds(self) -> None:
        root = ET.fromstring(render_systems("dark"))
        self.assertEqual(root.attrib["width"], "1200")
        self.assertEqual(root.attrib["height"], "420")
        modules = [
            node
            for node in root.iter("{http://www.w3.org/2000/svg}g")
            if "data-system" in node.attrib
        ]
        self.assertEqual(
            [node.attrib["data-system"] for node in modules],
            ["dag", "aviation", "jarvis"],
        )
        widths = [int(node.attrib["data-module-width"]) for node in modules]
        self.assertEqual(len(set(widths)), 3)
        self.assertGreater(widths[-1], max(widths[:-1]))
        evidence = {
            "".join(node.itertext()): float(node.attrib["x"])
            for node in root.iter("{http://www.w3.org/2000/svg}text")
        }
        self.assertGreaterEqual(
            evidence["~800 TB/day"] - evidence[">90% accuracy"],
            190,
        )
        for node in root.iter("{http://www.w3.org/2000/svg}text"):
            self.assertLessEqual(float(node.attrib["y"]), 420)

    def test_renderer_escapes_dynamic_text(self) -> None:
        svg = render_profile(self.data, "dark", status_label="A&B <ready>")
        self.assertIn("A&amp;B &lt;ready&gt;", svg)
        ET.fromstring(svg)

    def test_contribution_signal_is_hidden_below_threshold(self) -> None:
        quiet = ProfileData(stats=GitHubStats(99, 30))
        visible = ProfileData(stats=GitHubStats(100, 30))
        self.assertNotIn("CONTRIBUTIONS YTD", render_profile(quiet, "dark"))
        self.assertIn("100 CONTRIBUTIONS YTD", render_profile(visible, "dark"))

    def test_hero_geometry_and_hierarchy_are_explicit(self) -> None:
        svg = render_profile(self.data, "dark")
        root = ET.fromstring(svg)
        self.assertEqual(root.attrib["width"], "1200")
        self.assertEqual(root.attrib["height"], "560")
        self.assertLess(
            svg.index("Portrait of Divyanshu Goyal"),
            svg.index("DIVYANSHU GOYAL"),
        )
        self.assertLess(svg.index("DIVYANSHU GOYAL"), svg.index(">NNOMI</text>"))
        for node in root.iter("{http://www.w3.org/2000/svg}text"):
            self.assertLessEqual(float(node.attrib["y"]), 560)


if __name__ == "__main__":
    unittest.main()
