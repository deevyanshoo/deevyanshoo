from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Literal


Theme = Literal["light", "dark"]


@dataclass(frozen=True, slots=True)
class Palette:
    background: str
    surface: str
    ink: str
    secondary: str
    muted: str
    amber: str
    cyan: str
    line: str
    portrait: tuple[str, str, str, str]


PALETTES: dict[Theme, Palette] = {
    "dark": Palette(
        background="#080b0e",
        surface="#0d1116",
        ink="#f3f0e8",
        secondary="#c1c7cc",
        muted="#77828b",
        amber="#e6a23c",
        cyan="#69b8b0",
        line="#263039",
        portrait=("#182027", "#364149", "#77828b", "#d4d6d1"),
    ),
    "light": Palette(
        background="#f4f0e7",
        surface="#faf7f0",
        ink="#191d20",
        secondary="#3f474c",
        muted="#727b7e",
        amber="#a45d18",
        cyan="#2f7773",
        line="#d4cec2",
        portrait=("#d8d1c5", "#a89f91", "#706b64", "#292d2f"),
    ),
}


def palette(theme: Theme | str) -> Palette:
    try:
        return PALETTES[theme]  # type: ignore[index]
    except KeyError as error:
        raise ValueError("theme must be light or dark") from error


def text(
    x: int | float,
    y: int | float,
    value: str,
    css_class: str,
    fill: str,
    *,
    anchor: str | None = None,
    opacity: float | None = None,
) -> str:
    attributes = [f'class="{css_class}"', f'fill="{fill}"']
    if anchor:
        attributes.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attributes.append(f'opacity="{opacity:g}"')
    return (
        f'<text x="{x}" y="{y}" {" ".join(attributes)}>'
        f'{escape(value, quote=True)}</text>'
    )


def frame(
    theme: Theme,
    width: int,
    height: int,
    title: str,
    description: str,
    *,
    build_id: str = "dev",
) -> tuple[list[str], Palette]:
    colors = palette(theme)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" role="img" '
            f'data-theme="{theme}" data-build="{escape(build_id, quote=True)}">'
        ),
        f"<title>{escape(title)}</title>",
        f"<desc>{escape(description)}</desc>",
        "<style>",
        ".sans{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}",
        ".mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}",
        "</style>",
    ]
    return lines, colors
