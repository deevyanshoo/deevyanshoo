from __future__ import annotations

import unittest
from pathlib import Path

from operator_profile.fingerprint import SOURCE_INPUTS


ROOT = Path(__file__).resolve().parents[1]


class ReadmeContractTests(unittest.TestCase):
    def test_public_assets_exclude_internal_notes_and_vanity_metrics(self) -> None:
        names = (
            "profile-dark.svg", "profile-light.svg",
            "systems-dark.svg", "systems-light.svg",
        )
        public = [(ROOT / "README.md").read_text(encoding="utf-8")]
        public.extend((ROOT / "assets" / name).read_text(encoding="utf-8") for name in names)
        forbidden = (
            "approved portrait", "approved desk portrait", "image-derived",
            "source portrait", "privacy mode", "followers", "streak",
            "stars earned", "public repos", "language %",
        )
        combined = "\n".join(public).lower()
        for phrase in forbidden:
            self.assertNotIn(phrase, combined)

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
            "India-first financial coach",
            "Chauffit",
            "JARVIS",
            "DAG",
            "aviation",
            "University of Pennsylvania",
            "Gurugram ↔ wherever",
            "Current obsessions",
            "Outside the terminal",
            "F1",
            "watches",
            "garage target",
            "build weird things. make them useful. ship them.",
        ):
            self.assertIn(phrase, readme)
        self.assertLess(readme.index("## Building"), readme.index("## Things I built because I could"))
        self.assertLess(readme.index("Nnomi"), readme.index("Chauffit"))
        for forbidden in (
            "followers",
            "streak",
            "date of birth",
            "9 feb",
            "language %",
            "approved portrait",
            "approved desk portrait",
            "image-derived",
            "source portrait",
            "privacy mode",
            "live on android",
            "ios in progress",
            "x.com/divyanshoo",
            "### `01 /",
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
        self.assertIn('"scripts/generate.py"', profile)
        self.assertIn("schedule:", profile)
        self.assertIn("workflow_dispatch:", profile)
        self.assertIn("secrets.PROFILE_TOKEN", profile)
        self.assertIn('python -m pip install ".[portrait]"', ci)
        self.assertIn('python -m pip install ".[portrait]"', profile)
        self.assertNotIn('"assets/**"', profile)
        for relative in SOURCE_INPUTS:
            if relative.startswith("src/operator_profile/"):
                self.assertIn('"src/operator_profile/**"', profile)
            elif relative == "scripts/generate.py":
                self.assertIn('"scripts/generate.py"', profile)
        for asset in (
            "assets/profile-dark.svg",
            "assets/profile-light.svg",
            "assets/systems-dark.svg",
            "assets/systems-light.svg",
        ):
            self.assertIn(asset, profile)
            self.assertIn(f'cmp "$RUNNER_TEMP/profile-first/{Path(asset).name}"', ci)

    def test_token_documentation_requires_only_read_user_scope(self) -> None:
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("`read:user`", contributing)
        self.assertIn("no repository access", contributing.lower())
        self.assertNotIn("fine-grained personal access token", contributing.lower())


if __name__ == "__main__":
    unittest.main()
