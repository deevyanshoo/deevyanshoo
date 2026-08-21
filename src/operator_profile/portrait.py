from __future__ import annotations

from .portrait_data import TONE_RUNS
from .svg import Palette


def _path_data(runs: tuple[tuple[int, int, int], ...]) -> str:
    return " ".join(
        f"M{x} {y}h{length}v1h-{length}z"
        for y, x, length in runs
    )


def render_portrait(
    colors: Palette,
    x: int,
    y: int,
    *,
    scale: float = 2,
) -> list[str]:
    lines = [
        (
            f'<g transform="translate({x} {y}) scale({scale:g})" '
            'role="img" aria-label="Portrait of Divyanshu Goyal" '
            'shape-rendering="crispEdges">'
        )
    ]
    for fill, runs in zip(colors.portrait, TONE_RUNS, strict=True):
        lines.append(f'<path d="{_path_data(runs)}" fill="{fill}"/>')
    lines.append("</g>")
    return lines
