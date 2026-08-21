from __future__ import annotations

import unittest

from operator_profile.svg import palette, text


class SvgPrimitiveTests(unittest.TestCase):
    def test_palette_rejects_unknown_theme(self) -> None:
        with self.assertRaisesRegex(ValueError, "light or dark"):
            palette("sepia")

    def test_themes_are_independently_authored(self) -> None:
        light = palette("light")
        dark = palette("dark")
        self.assertNotEqual(light.background, dark.background)
        self.assertNotEqual(light.ink, dark.ink)
        self.assertNotEqual(light.amber, dark.amber)
        self.assertNotEqual(light.cyan, dark.cyan)

    def test_text_escapes_dynamic_values(self) -> None:
        value = text(10, 20, "A&B <ready>", "sans body", "#fff")
        self.assertIn("A&amp;B &lt;ready&gt;", value)
        self.assertNotIn("A&B <ready>", value)


if __name__ == "__main__":
    unittest.main()
