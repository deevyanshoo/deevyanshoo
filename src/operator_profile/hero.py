from __future__ import annotations

from .content import (
    EASTER_EGGS,
    EDUCATION,
    LOCATION,
    MISSION_JOURNEY,
    MISSION_LINE,
    MISSION_NAME,
    MISSION_URL,
    NAME,
    ROLE,
    TAGLINE,
    WORK,
)
from .model import ProfileData
from .portrait import render_portrait
from .svg import Palette, Theme, frame, text


WIDTH = 1200
HEIGHT = 560
CONTRIBUTION_THRESHOLD = 100


def _journey(colors: Palette) -> list[str]:
    amber = colors.amber
    cyan = colors.cyan
    line = colors.line
    muted = colors.muted
    secondary = colors.secondary
    points = (452, 586, 735, 877, 1049)
    lines = [
        f'<line x1="{points[0]}" y1="425" x2="{points[-1]}" y2="425" '
        f'stroke="{line}" stroke-width="2"/>',
        f'<line x1="{points[0]}" y1="425" x2="{points[2]}" y2="425" '
        f'stroke="{amber}" stroke-width="2"/>',
        f'<line x1="{points[2]}" y1="425" x2="{points[-1]}" y2="425" '
        f'stroke="{cyan}" stroke-width="2"/>',
    ]
    for index, (step, x) in enumerate(zip(MISSION_JOURNEY, points, strict=True)):
        color = amber if index < 3 else cyan
        lines.extend(
            (
                f'<circle cx="{x}" cy="425" r="5" fill="{color}"/>',
                text(x, 452, step.label, "mono journey-label", secondary, anchor="middle"),
                text(x, 470, step.emphasis, "sans journey-detail", muted, anchor="middle"),
            )
        )
    return lines


def render_hero(
    data: ProfileData,
    theme: Theme,
    *,
    status_label: str = "LIVE",
    build_id: str = "dev",
) -> str:
    lines, colors = frame(
        theme,
        WIDTH,
        HEIGHT,
        "Divyanshu Goyal - AI architect, founder, builder",
        (
            "Divyanshu Goyal builds ambitious AI systems and Nnomi, "
            "an India-first financial coach."
        ),
        build_id=build_id,
    )
    lines.extend(
        (
            "<style>",
            ".name{font-size:55px;font-weight:780;letter-spacing:-2px}",
            ".role{font-size:13px;font-weight:720;letter-spacing:1.8px}",
            ".tagline{font-size:27px;font-weight:650;letter-spacing:-.5px}",
            ".context{font-size:11px;font-weight:650;letter-spacing:1.15px}",
            ".mission-name{font-size:48px;font-weight:800;letter-spacing:-1.4px}",
            ".mission-line{font-size:18px;font-weight:540}",
            ".journey-label{font-size:10px;font-weight:700;letter-spacing:.75px}",
            ".journey-detail{font-size:10px}",
            ".micro{font-size:10px;letter-spacing:.65px}",
            "</style>",
            "<defs>",
            (
                '<linearGradient id="portrait-field" x1="0" y1="0" x2="1" y2="1">'
                f'<stop stop-color="{colors.surface}"/>'
                f'<stop offset="1" stop-color="{colors.background}"/>'
                "</linearGradient>"
            ),
            "</defs>",
            f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{colors.background}"/>',
            (
                f'<rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" '
                f'rx="17" fill="none" stroke="{colors.line}"/>'
            ),
            f'<path d="M24 31H1176" stroke="{colors.line}"/>',
            f'<rect x="24" y="54" width="374" height="444" rx="10" fill="url(#portrait-field)"/>',
            f'<path d="M398 54V498" stroke="{colors.line}"/>',
            f'<path d="M24 498H1176" stroke="{colors.line}"/>',
            text(24, 22, "DEEVYANSHOO", "mono micro", colors.muted),
            text(1176, 22, "AI SYSTEMS / PRODUCTS / ODD EXPERIMENTS", "mono micro", colors.muted, anchor="end"),
        )
    )
    lines.extend(render_portrait(colors, 38, 63, scale=2))
    lines.extend(
        (
            text(438, 103, NAME, "sans name", colors.ink),
            text(440, 134, ROLE, "sans role", colors.amber),
            text(440, 188, TAGLINE, "sans tagline", colors.ink),
            text(440, 224, EDUCATION, "mono context", colors.muted),
            text(440, 244, WORK, "mono context", colors.muted),
            text(1176, 244, LOCATION, "mono context", colors.cyan, anchor="end"),
            f'<path d="M440 268H1176" stroke="{colors.line}"/>',
            text(440, 301, "BUILDING NOW", "mono context", colors.amber),
            text(440, 350, MISSION_NAME, "sans mission-name", colors.ink),
            text(1176, 347, MISSION_URL, "mono context", colors.cyan, anchor="end"),
            text(440, 383, MISSION_LINE, "sans mission-line", colors.secondary),
        )
    )
    lines.extend(_journey(colors))
    if data.stats.contributions_ytd >= CONTRIBUTION_THRESHOLD:
        lines.append(
            text(
                1176,
                282,
                f"{status_label} \u00b7 {data.stats.contributions_ytd:,} CONTRIBUTIONS YTD",
                "mono micro",
                colors.muted,
                anchor="end",
            )
        )
    egg_positions = (24, 302, 540, 896)
    for value, x in zip(EASTER_EGGS, egg_positions, strict=True):
        color = colors.amber if x in (24, 896) else colors.muted
        lines.append(text(x, 536, value, "mono micro", color))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"
