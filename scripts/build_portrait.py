from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


PORTRAIT_SIZE = (168, 216)
THRESHOLDS = (58, 112, 174)


@dataclass(frozen=True, slots=True)
class Crop:
    left: int
    top: int
    right: int
    bottom: int

    def as_box(self) -> tuple[int, int, int, int]:
        return self.left, self.top, self.right, self.bottom


DEFAULT_CROP = Crop(430, 20, 1180, 985)


def _validate_crop(image: Image.Image, crop: Crop) -> None:
    if crop.left >= crop.right or crop.top >= crop.bottom:
        raise ValueError("crop must have positive width and height")
    if crop.left < 0 or crop.top < 0:
        raise ValueError("crop must remain within image bounds")
    if crop.right > image.width or crop.bottom > image.height:
        raise ValueError("crop exceeds image bounds")


def quantize_portrait(
    image: Image.Image,
    crop: Crop,
    *,
    size: tuple[int, int] = PORTRAIT_SIZE,
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    image = ImageOps.exif_transpose(image)
    _validate_crop(image, crop)
    sample = image.crop(crop.as_box()).convert("L")
    sample = sample.resize(size, Image.Resampling.LANCZOS)
    sample = ImageOps.autocontrast(sample, cutoff=1)
    sample = sample.filter(ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=3))

    width, height = size
    pixels = list(sample.get_flattened_data())
    layers: list[list[tuple[int, int, int]]] = [[], [], [], []]
    for y in range(height):
        row = pixels[y * width : (y + 1) * width]
        tones = [
            0 if value < THRESHOLDS[0]
            else 1 if value < THRESHOLDS[1]
            else 2 if value < THRESHOLDS[2]
            else 3
            for value in row
        ]
        start = 0
        while start < width:
            tone = tones[start]
            end = start + 1
            while end < width and tones[end] == tone:
                end += 1
            layers[tone].append((y, start, end - start))
            start = end
    return tuple(tuple(layer) for layer in layers)


def _module_text(
    layers: tuple[tuple[tuple[int, int, int], ...], ...],
    size: tuple[int, int],
) -> str:
    width, height = size
    lines = [
        "from __future__ import annotations",
        "",
        "# Generated deterministically by scripts/build_portrait.py.",
        f"PORTRAIT_SIZE = ({width}, {height})",
        "TONE_RUNS = (",
    ]
    for layer in layers:
        lines.append("    (")
        for run in layer:
            lines.append(f"        {run},")
        lines.append("    ),")
    lines.extend((")", ""))
    return "\n".join(lines)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build deterministic four-tone vector runs for the profile portrait."
    )
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--crop",
        type=int,
        nargs=4,
        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
        default=DEFAULT_CROP.as_box(),
    )
    return parser.parse_args()


def main() -> int:
    arguments = _arguments()
    crop = Crop(*arguments.crop)
    with Image.open(arguments.source) as image:
        layers = quantize_portrait(image, crop)
    content = _module_text(layers, PORTRAIT_SIZE)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(arguments.output)
    print(
        f"wrote {arguments.output} "
        f"({sum(len(layer) for layer in layers):,} vector runs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
