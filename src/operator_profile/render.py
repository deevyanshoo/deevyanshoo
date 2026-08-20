from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Literal

from .content import (
    CURRENT_MISSION,
    LOCATION,
    NAME,
    POSITIONING,
    ROLE,
    SECONDARY_MISSION,
    SELECTED_BUILDS,
    TAGLINE,
)
from .model import ProfileData
from .portrait import PORTRAIT


Theme = Literal["light", "dark"]


@dataclass(frozen=True, slots=True)
class Palette:
    background: str
    panel: str
    border: str
    primary: str
    secondary: str
    muted: str
    accent: str
    signal: str


PALETTES: dict[Theme, Palette] = {
    "dark": Palette("#0d1117", "#111820", "#30363d", "#f0f6fc", "#c9d1d9", "#8b949e", "#58a6ff", "#3fb950"),
    "light": Palette("#ffffff", "#f6f8fa", "#d0d7de", "#1f2328", "#3b434b", "#656d76", "#0969da", "#1a7f37"),
}


def _text(x: int, y: int, value: str, css_class: str = "body", anchor: str | None = None) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" class="{css_class}"{anchor_attr}>{escape(value, quote=True)}</text>'


def _metric(x: int, y: int, label: str, value: str) -> list[str]:
    return [
        _text(x, y, label.upper(), "metric-label"),
        _text(x + 196, y, value, "metric-value", "end"),
    ]


def render_profile(data: ProfileData, theme: Theme, *, status_label: str = "ONLINE") -> str:
    if theme not in PALETTES:
        raise ValueError("theme must be 'light' or 'dark'")
    palette = PALETTES[theme]
    stats = data.stats
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" data-theme="{theme}">',
        "<title>Divyanshu Goyal — AI architect, founder, and builder</title>",
        "<desc>Operator console featuring an ASCII portrait, current AI and founder work, selected systems, and anonymous aggregate GitHub telemetry.</desc>",
        "<style>",
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace}",
        ".eyebrow{font-size:13px;font-weight:700;letter-spacing:2.2px}",
        ".title{font-size:32px;font-weight:800;letter-spacing:.4px}",
        ".role{font-size:15px;font-weight:700;letter-spacing:1.2px}",
        ".tagline{font-size:18px;font-weight:700}",
        ".body{font-size:14px}",
        ".small{font-size:12px}",
        ".section{font-size:12px;font-weight:800;letter-spacing:2px}",
        ".metric-label{font-size:11px;letter-spacing:1px}",
        ".metric-value{font-size:14px;font-weight:800}",
        ".portrait{font-size:13px;white-space:pre}",
        "</style>",
        f'<rect width="1200" height="800" rx="18" fill="{palette.background}"/>',
        f'<rect x="18" y="18" width="1164" height="764" rx="14" fill="{palette.panel}" stroke="{palette.border}"/>',
        f'<g fill="{palette.muted}">', _text(48, 56, "DEEVYANSHOO // OPERATOR", "eyebrow"), "</g>",
        f'<circle cx="1078" cy="51" r="5" fill="{palette.signal}"/>',
        f'<g fill="{palette.signal}">', _text(1092, 56, status_label, "eyebrow"), "</g>",
        f'<line x1="48" y1="78" x2="1152" y2="78" stroke="{palette.border}"/>',
        f'<g fill="{palette.accent}">', _text(48, 112, "PORTRAIT / 01", "section"), "</g>",
        f'<g fill="{palette.secondary}">',
    ]
    for index, row in enumerate(PORTRAIT):
        lines.append(_text(48, 144 + index * 16, row, "portrait"))
    lines.extend([
        "</g>",
        f'<line x1="488" y1="102" x2="488" y2="526" stroke="{palette.border}"/>',
        f'<g fill="{palette.accent}">', _text(526, 112, "IDENTITY / MISSION", "section"), "</g>",
        f'<g fill="{palette.primary}">', _text(526, 154, NAME, "title"), "</g>",
        f'<g fill="{palette.accent}">', _text(526, 184, ROLE, "role"), "</g>",
        f'<g fill="{palette.secondary}">', _text(526, 218, POSITIONING, "body"), "</g>",
        f'<g fill="{palette.primary}">', _text(526, 252, TAGLINE, "tagline"), "</g>",
        f'<g fill="{palette.muted}">',
        _text(526, 278, "AI Architect @ ZS  ·  UPenn MSE Data Science", "small"),
        _text(526, 300, LOCATION, "small"), "</g>",
        f'<line x1="526" y1="326" x2="1152" y2="326" stroke="{palette.border}"/>',
        f'<g fill="{palette.accent}">', _text(526, 354, "CURRENT", "section"), "</g>",
        f'<g fill="{palette.primary}">', _text(526, 386, CURRENT_MISSION, "body"), "</g>",
        f'<g fill="{palette.secondary}">', _text(526, 412, SECONDARY_MISSION, "body"), "</g>",
        f'<g fill="{palette.accent}">', _text(526, 456, "SELECTED BUILDS", "section"), "</g>",
    ])
    build_y = 486
    for build in SELECTED_BUILDS:
        lines.extend([
            f'<g fill="{palette.primary}">', _text(526, build_y, build.label, "body"), "</g>",
            f'<g fill="{palette.muted}">', _text(650, build_y, build.detail, "small"), "</g>",
        ])
        build_y += 26
    lines.extend([
        f'<line x1="48" y1="566" x2="1152" y2="566" stroke="{palette.border}"/>',
        f'<g fill="{palette.accent}">', _text(48, 596, "GITHUB / LIVE AGGREGATES", "section"), "</g>",
        f'<g fill="{palette.muted}">',
    ])
    metrics = (
        (48, 630, "CONTRIBUTIONS YTD", f"{stats.contributions_ytd:,}"),
        (300, 630, "MERGED PRS", f"{stats.merged_pull_requests:,}"),
        (552, 630, "PUBLIC REPOS", f"{stats.public_repositories:,}"),
        (804, 630, "RECENT REPOS", f"{stats.repositories_contributed_to:,}"),
        (48, 676, "STARS EARNED", f"{stats.stars_earned:,}"),
        (300, 676, "PRIVACY MODE", "AGGREGATE ONLY"),
    )
    for x, y, label, value in metrics:
        lines.extend(_metric(x, y, label, value))
    lines.extend([
        "</g>",
        f'<line x1="48" y1="716" x2="1152" y2="716" stroke="{palette.border}"/>',
        f'<g fill="{palette.muted}">',
        _text(48, 750, "coffee ........ required", "small"),
        _text(332, 750, "inference ..... local > cloud", "small"),
        _text(676, 750, "runtime ........ v26", "small"),
        _text(936, 750, "garage_target .. 911", "small"),
        "</g>", "</svg>",
    ])
    return "\n".join(lines) + "\n"
