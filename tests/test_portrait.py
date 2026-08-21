from __future__ import annotations

import unittest
import warnings

from PIL import Image

from scripts.build_portrait import Crop, DEFAULT_CROP, quantize_portrait
from operator_profile.portrait import render_portrait
from operator_profile.portrait_data import PORTRAIT_SIZE, TONE_RUNS
from operator_profile.svg import palette


class PortraitPipelineTests(unittest.TestCase):
    def test_quantization_is_deterministic_and_has_four_layers(self) -> None:
        image = Image.new("L", (8, 8))
        image.putdata([(x * 31 + y * 17) % 256 for y in range(8) for x in range(8)])
        crop = Crop(0, 0, 8, 8)
        first = quantize_portrait(image, crop, size=(8, 8))
        second = quantize_portrait(image, crop, size=(8, 8))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 4)
        self.assertTrue(all(layer for layer in first))

    def test_quantization_uses_supported_pillow_apis(self) -> None:
        image = Image.new("L", (8, 8), 128)
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            layers = quantize_portrait(image, Crop(0, 0, 8, 8), size=(8, 8))
        self.assertEqual(len(layers), 4)

    def test_quantization_rejects_invalid_crop(self) -> None:
        image = Image.new("RGB", (20, 20), "white")
        with self.assertRaisesRegex(ValueError, "crop"):
            quantize_portrait(image, Crop(10, 10, 9, 19))
        with self.assertRaisesRegex(ValueError, "bounds"):
            quantize_portrait(image, Crop(0, 0, 21, 20))

    def test_committed_vector_data_is_dense_and_bounded(self) -> None:
        width, height = PORTRAIT_SIZE
        self.assertEqual((width, height), (168, 216))
        self.assertEqual(len(TONE_RUNS), 4)
        self.assertGreater(sum(len(layer) for layer in TONE_RUNS), 500)
        for layer in TONE_RUNS:
            for y, x, length in layer:
                self.assertGreater(length, 0)
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x + length, width)
                self.assertLess(y, height)

    def test_default_crop_is_head_and_shoulders(self) -> None:
        self.assertLessEqual(DEFAULT_CROP.bottom, 820)
        self.assertLess(DEFAULT_CROP.right - DEFAULT_CROP.left, 650)

    def test_portrait_renderer_emits_one_path_per_tone(self) -> None:
        rendered = "\n".join(render_portrait(palette("dark"), 24, 40, scale=2))
        self.assertEqual(rendered.count("<path "), 4)
        self.assertIn('aria-label="Portrait of Divyanshu Goyal"', rendered)
        self.assertIn('shape-rendering="crispEdges"', rendered)


if __name__ == "__main__":
    unittest.main()
