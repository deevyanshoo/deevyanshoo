from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from operator_profile.fingerprint import source_fingerprint


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
            first = {
                theme: (output / f"profile-{theme}.svg").read_bytes()
                for theme in ("light", "dark")
            }
            subprocess.run(command, cwd=ROOT, env=environment, check=True)
            second = {
                theme: (output / f"profile-{theme}.svg").read_bytes()
                for theme in ("light", "dark")
            }

            self.assertEqual(first, second)
            self.assertTrue(all(value.startswith(b"<?xml") for value in first.values()))


if __name__ == "__main__":
    unittest.main()
