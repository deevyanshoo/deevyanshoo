from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from operator_profile.fingerprint import SOURCE_INPUTS, source_fingerprint


ROOT = Path(__file__).resolve().parents[1]


class GeneratorContractTests(unittest.TestCase):
    def test_source_fingerprint_is_stable_and_input_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.py").write_text("alpha", encoding="utf-8")
            (root / "two.py").write_text("beta", encoding="utf-8")
            inputs = ("one.py", "two.py")
            first = source_fingerprint(root, inputs)
            self.assertEqual(first, source_fingerprint(root, inputs))
            self.assertRegex(first, r"^[0-9a-f]{12}$")
            (root / "two.py").write_text("changed", encoding="utf-8")
            self.assertNotEqual(first, source_fingerprint(root, inputs))

    def test_source_fingerprint_is_independent_of_checkout_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "renderer.py"
            path.write_bytes(b"alpha\r\nbeta\r\n")
            windows = source_fingerprint(root, ("renderer.py",))
            path.write_bytes(b"alpha\nbeta\n")
            self.assertEqual(windows, source_fingerprint(root, ("renderer.py",)))

    def test_offline_generation_is_byte_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "scripts" / "generate.py"),
                "--offline",
                "--output-dir",
                str(output),
            ]
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(ROOT / "src")

            subprocess.run(command, cwd=ROOT, env=environment, check=True)
            names = (
                "profile-light.svg",
                "profile-dark.svg",
                "systems-light.svg",
                "systems-dark.svg",
            )
            first = {name: (output / name).read_bytes() for name in names}
            subprocess.run(command, cwd=ROOT, env=environment, check=True)
            second = {name: (output / name).read_bytes() for name in names}

            self.assertEqual(first, second)
            self.assertTrue(all(value.startswith(b"<?xml") for value in first.values()))
            build = source_fingerprint(ROOT).encode()
            self.assertTrue(all(b'data-build="' + build + b'"' in value for value in first.values()))

    def test_committed_assets_match_current_source_fingerprint(self) -> None:
        expected = source_fingerprint(ROOT)
        self.assertEqual(len(SOURCE_INPUTS), len(set(SOURCE_INPUTS)))
        for name in (
            "profile-light.svg",
            "profile-dark.svg",
            "systems-light.svg",
            "systems-dark.svg",
        ):
            content = (ROOT / "assets" / name).read_text(encoding="utf-8")
            self.assertIn(f'data-build="{expected}"', content, name)


if __name__ == "__main__":
    unittest.main()
