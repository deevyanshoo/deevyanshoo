from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeContractTests(unittest.TestCase):
    def test_readme_has_theme_art_and_native_accessible_story(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        lower = readme.lower()
        self.assertIn("<picture>", readme)
        self.assertIn("assets/profile-dark.svg", readme)
        self.assertIn("assets/profile-light.svg", readme)
        self.assertIn("assets/systems-dark.svg", readme)
        self.assertIn("assets/systems-light.svg", readme)
        self.assertIn('alt="Divyanshu Goyal', readme)
        for phrase in (
            "Nnomi",
            "Chauffit",
            "JARVIS",
            "DAG",
            "aviation",
            "University of Pennsylvania",
            "Gurugram ↔ wherever",
            "CURRENT OBSESSIONS",
            "OUTSIDE THE TERMINAL",
            "F1",
            "watches",
            "garage target",
            "build weird things. make them useful. ship them.",
        ):
            self.assertIn(phrase, readme)
        for forbidden in (
            "followers",
            "streak",
            "date of birth",
            "9 feb",
            "language %",
            "approved portrait",
            "approved desk portrait",
            "image-derived",
        ):
            self.assertNotIn(forbidden, lower)

    def test_ci_and_profile_workflows_separate_permissions_and_secrets(self) -> None:
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        profile = (ROOT / ".github" / "workflows" / "profile.yml").read_text(
            encoding="utf-8"
        )
        for workflow in (ci, profile):
            self.assertIn("actions/checkout@v7", workflow)
            self.assertIn("actions/setup-python@v7", workflow)
        self.assertIn("contents: read", ci)
        self.assertNotIn("PROFILE_TOKEN", ci)
        self.assertIn('--output-dir "$RUNNER_TEMP/profile-first"', ci)
        self.assertIn('--output-dir "$RUNNER_TEMP/profile-second"', ci)
        self.assertNotIn("git diff --exit-code -- assets", ci)
        self.assertNotIn("pull_request", profile)
        self.assertIn("contents: write", profile)
        self.assertIn("push:", profile)
        self.assertIn('"src/operator_profile/**"', profile)
        self.assertIn("schedule:", profile)
        self.assertIn("workflow_dispatch:", profile)
        self.assertIn("secrets.PROFILE_TOKEN", profile)
        for asset in (
            "assets/profile-dark.svg",
            "assets/profile-light.svg",
            "assets/systems-dark.svg",
            "assets/systems-light.svg",
        ):
            self.assertIn(asset, profile)

    def test_token_documentation_requires_only_read_user_scope(self) -> None:
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("`read:user`", contributing)
        self.assertIn("no repository access", contributing.lower())
        self.assertNotIn("fine-grained personal access token", contributing.lower())


if __name__ == "__main__":
    unittest.main()
