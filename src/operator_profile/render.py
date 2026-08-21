from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Literal

from .content import (
    CURRENT_MISSION,
    CURRENT_MISSION_LINE_1,
    CURRENT_MISSION_LINE_2,
    CURRENT_MISSION_URL,
    LOCATION,
    NAME,
    POSITIONING,
    ROLE,
    SECONDARY_MISSION,
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
    amber: str
    cyan: str
    signal: str
    grid: str


PALETTES: dict[Theme, Palette] = {
    "dark": Palette(
        "#090d12", "#0c1218", "#24303a", "#f5f7fa", "#cbd5df",
        "#7f8a98", "#ffb000", "#63d5c3", "#7ee787", "#15202a",
    ),
    "light": Palette(
        "#fbfcfe", "#ffffff", "#d8dee7", "#111827", "#374151",
        "#6b7280", "#a66200", "#087f78", "#15803d", "#edf1f5",
    ),
}


def _text(
    x: int,
    y: int,
    value: str,
    css_class: str,
    *,
    fill: str,
    anchor: str | None = None,
    opacity: float | None = None,
) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    opacity_attr = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<text x="{x}" y="{y}" class="{css_class}" fill="{fill}"'
        f'{anchor_attr}{opacity_attr}>{escape(value, quote=True)}</text>'
    )


def _header(theme: Theme, *, width: int, height: int, title: str, desc: str) -> tuple[list[str], Palette]:
    if theme not in PALETTES:
        raise ValueError("theme must be 'light' or 'dark'")
    palette = PALETTES[theme]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" data-theme="{theme}">'
        ),
        f"<title>{escape(title)}</title>",
        f"<desc>{escape(desc)}</desc>",
        "<defs>",
        (
            f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
            f'<path d="M32 0H0V32" fill="none" stroke="{palette.grid}" stroke-width="1"/>'
            "</pattern>"
        ),
        (
            f'<linearGradient id="pulse" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{palette.amber}"/>'
            f'<stop offset="1" stop-color="{palette.cyan}"/>'
            "</linearGradient>"
        ),
        "</defs>",
        "<style>",
        ".sans{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Arial,sans-serif}",
        ".mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace}",
        ".name{font-size:48px;font-weight:800;letter-spacing:-1.4px}",
        ".role{font-size:14px;font-weight:700;letter-spacing:1.6px}",
        ".eyebrow{font-size:13px;font-weight:700;letter-spacing:1.8px}",
        ".tag{font-size:25px;font-weight:700;letter-spacing:-.4px}",
        ".body{font-size:15px}",
        ".small{font-size:12px}",
        ".micro{font-size:11px;letter-spacing:.7px}",
        ".portrait{font-size:13px;white-space:pre;font-weight:700}",
        ".mission{font-size:28px;font-weight:800;letter-spacing:-.4px}",
        ".card-title{font-size:22px;font-weight:800}",
        ".metric{font-size:24px;font-weight:800}",
        "</style>",
        f'<rect width="{width}" height="{height}" rx="18" fill="{palette.background}"/>',
        (
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" '
            f'fill="{palette.panel}" stroke="{palette.border}"/>'
        ),
        (
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" '
            'fill="url(#grid)" opacity=".45"/>'
        ),
    ]
    return lines, palette


def render_profile(
    data: ProfileData,
    theme: Theme,
    *,
    status_label: str = "LIVE",
) -> str:
    lines, palette = _header(
        theme,
        width=1200,
        height=520,
        title="Divyanshu Goyal — AI architect, founder, builder",
        desc=(
            "Operator console with an image-derived ASCII portrait, Nnomi current "
            "mission, AI systems focus, and live aggregate GitHub activity."
        ),
    )
    stats = data.stats

    lines.extend([
        f'<line x1="28" y1="54" x2="1172" y2="54" stroke="{palette.border}"/>',
        _text(30, 35, "deevyanshoo@operator", "mono eyebrow", fill=palette.muted),
        f'<circle cx="922" cy="31" r="4" fill="{palette.signal}"/>',
        _text(
            936,
            35,
            (
                f"{status_label}  //  {stats.contributions_ytd:,} CONTRIB YTD  //  "
                f"{stats.merged_pull_requests:,} MERGED PRS"
            ),
            "mono micro",
            fill=palette.muted,
        ),
        f'<line x1="432" y1="76" x2="432" y2="458" stroke="{palette.border}"/>',
        _text(30, 84, "PORTRAIT // ASCII SCAN", "mono eyebrow", fill=palette.cyan),
    ])

    y = 108
    for row in PORTRAIT:
        lines.append(
            _text(30, y, row, "mono portrait", fill=palette.secondary, opacity=0.82)
        )
        y += 13

    lines.extend([
        _text(
            30,
            476,
            "image-derived // approved portrait",
            "mono micro",
            fill=palette.muted,
        ),
        _text(470, 86, "IDENTITY // 00", "mono eyebrow", fill=palette.cyan),
        _text(470, 137, NAME, "sans name", fill=palette.primary),
        _text(470, 169, ROLE, "mono role", fill=palette.amber),
        _text(470, 218, TAGLINE, "sans tag", fill=palette.primary),
        _text(470, 246, POSITIONING, "sans body", fill=palette.secondary),
        f'<line x1="470" y1="274" x2="1168" y2="274" stroke="{palette.border}"/>',
        _text(
            470,
            302,
            f"CURRENT MISSION // {CURRENT_MISSION}",
            "mono eyebrow",
            fill=palette.amber,
        ),
        _text(470, 338, CURRENT_MISSION, "sans mission", fill=palette.primary),
        _text(590, 336, CURRENT_MISSION_URL, "mono small", fill=palette.cyan),
        _text(470, 365, CURRENT_MISSION_LINE_1, "sans body", fill=palette.secondary),
        _text(470, 387, CURRENT_MISSION_LINE_2, "sans body", fill=palette.secondary),
    ])

    nodes = (
        ("EARN", 490),
        ("SPEND", 625),
        ("PROTECT", 770),
        ("INVEST", 930),
        ("WEALTH", 1080),
    )
    line_y = 414
    for index, (label, x) in enumerate(nodes):
        if index < len(nodes) - 1:
            next_x = nodes[index + 1][1]
            lines.append(
                f'<line x1="{x}" y1="{line_y}" x2="{next_x}" y2="{line_y}" '
                'stroke="url(#pulse)" stroke-width="2" opacity=".72"/>'
            )
        color = palette.amber if index < 3 else palette.cyan
        lines.append(f'<circle cx="{x}" cy="{line_y}" r="5" fill="{color}"/>')
        lines.append(
            _text(
                x,
                line_y + 22,
                label,
                "mono micro",
                fill=palette.muted,
                anchor="middle",
            )
        )

    lines.extend([
        _text(470, 462, f"also building // {SECONDARY_MISSION}", "mono small", fill=palette.secondary),
        f'<line x1="28" y1="490" x2="1172" y2="490" stroke="{palette.border}"/>',
        _text(30, 510, LOCATION, "mono micro", fill=palette.muted),
        _text(220, 510, "MSE // PENN", "mono micro", fill=palette.muted),
        _text(350, 510, "AI ARCHITECT @ ZS", "mono micro", fill=palette.muted),
        _text(540, 510, "runtime v26", "mono micro", fill=palette.muted),
        _text(690, 510, "inference local > cloud", "mono micro", fill=palette.muted),
        _text(930, 510, "garage_target 911", "mono micro", fill=palette.amber),
        "</svg>",
    ])
    return "\n".join(lines) + "\n"


def render_systems(theme: Theme) -> str:
    lines, palette = _header(
        theme,
        width=1200,
        height=360,
        title="Things I built because I could",
        desc=(
            "Three selected technical systems: JARVIS hybrid inference, a DAG ledger, "
            "and large-scale aviation forecasting."
        ),
    )

    lines.extend([
        _text(
            28,
            36,
            "THINGS I BUILT BECAUSE I COULD // 02",
            "mono eyebrow",
            fill=palette.amber,
        ),
        _text(
            1170,
            36,
            "distributed systems  >  large-scale ML  >  edge AI",
            "mono small",
            fill=palette.muted,
            anchor="end",
        ),
        f'<line x1="28" y1="54" x2="1172" y2="54" stroke="{palette.border}"/>',
        f'<line x1="400" y1="78" x2="400" y2="316" stroke="{palette.border}"/>',
        f'<line x1="800" y1="78" x2="800" y2="316" stroke="{palette.border}"/>',

        _text(28, 88, "01 // JARVIS", "mono eyebrow", fill=palette.cyan),
        _text(28, 120, "HYBRID AI", "sans card-title", fill=palette.primary),
        _text(28, 146, "personal assistant on a phone", "sans body", fill=palette.secondary),
        f'<rect x="44" y="178" width="74" height="102" rx="12" fill="none" stroke="{palette.secondary}" stroke-width="2"/>',
        f'<rect x="65" y="188" width="32" height="5" rx="2" fill="{palette.muted}"/>',
        f'<circle cx="81" cy="266" r="4" fill="{palette.muted}"/>',
        _text(81, 224, "J", "sans metric", fill=palette.amber, anchor="middle"),
        f'<rect x="155" y="205" width="82" height="46" rx="8" fill="none" stroke="{palette.amber}" stroke-width="1.5"/>',
        _text(196, 232, "ROUTER", "mono small", fill=palette.amber, anchor="middle"),
        f'<line x1="118" y1="229" x2="155" y2="229" stroke="{palette.muted}" stroke-width="1.5"/>',
        f'<line x1="237" y1="217" x2="290" y2="190" stroke="{palette.amber}" stroke-width="1.5"/>',
        f'<line x1="237" y1="239" x2="290" y2="265" stroke="{palette.cyan}" stroke-width="1.5"/>',
        f'<rect x="290" y="168" width="82" height="45" rx="7" fill="none" stroke="{palette.amber}"/>',
        _text(331, 188, "LOCAL", "mono small", fill=palette.amber, anchor="middle"),
        _text(331, 204, "SLM", "mono small", fill=palette.secondary, anchor="middle"),
        f'<rect x="290" y="244" width="82" height="45" rx="7" fill="none" stroke="{palette.cyan}"/>',
        _text(331, 264, "CLOUD", "mono small", fill=palette.cyan, anchor="middle"),
        _text(331, 280, "LLM", "mono small", fill=palette.secondary, anchor="middle"),
        _text(28, 318, "privacy HIGH // latency LOW // cloud optional", "mono small", fill=palette.muted),

        _text(428, 88, "02 // DAG LEDGER", "mono eyebrow", fill=palette.cyan),
        _text(428, 120, "DISTRIBUTED SYSTEMS", "sans card-title", fill=palette.primary),
        _text(
            428,
            146,
            "peer-approved blocks without a linear chain",
            "sans body",
            fill=palette.secondary,
        ),
    ])

    nodes = {
        "a": (475, 205),
        "b": (560, 176),
        "c": (645, 210),
        "d": (535, 265),
        "e": (690, 270),
        "f": (745, 188),
    }
    edges = (
        ("a", "b"),
        ("a", "d"),
        ("b", "c"),
        ("b", "d"),
        ("c", "d"),
        ("c", "f"),
        ("c", "e"),
        ("d", "e"),
        ("f", "e"),
    )
    for left, right in edges:
        x1, y1 = nodes[left]
        x2, y2 = nodes[right]
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{palette.muted}" stroke-width="1.5" opacity=".75"/>'
        )
    for index, (_, (x, y)) in enumerate(nodes.items()):
        color = palette.amber if index in (0, 1, 3) else palette.cyan
        lines.append(
            f'<circle cx="{x}" cy="{y}" r="8" fill="{palette.panel}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        lines.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')

    lines.extend([
        _text(
            428,
            318,
            "DAG growth // P2P approvals // custom consensus",
            "mono small",
            fill=palette.muted,
        ),

        _text(828, 88, "03 // AVIATION", "mono eyebrow", fill=palette.cyan),
        _text(828, 120, "FORECASTING AT SCALE", "sans card-title", fill=palette.primary),
        _text(828, 146, "demand prediction 65 days ahead", "sans body", fill=palette.secondary),
        _text(828, 200, ">90%", "sans metric", fill=palette.amber),
        _text(910, 198, "forecast accuracy", "mono small", fill=palette.muted),
        _text(828, 238, "~800 TB/day", "sans metric", fill=palette.primary),
        _text(970, 236, "data environment", "mono small", fill=palette.muted),
        f'<line x1="828" y1="285" x2="1150" y2="285" stroke="{palette.border}"/>',
        f'<line x1="975" y1="260" x2="975" y2="306" stroke="{palette.border}" stroke-dasharray="4 4"/>',
        (
            f'<polyline points="828,287 860,272 892,279 924,248 956,259 988,240 '
            f'1020,246 1052,220 1084,229 1116,208 1148,214" fill="none" '
            f'stroke="{palette.secondary}" stroke-width="2"/>'
        ),
        (
            f'<polyline points="975,257 1008,246 1041,236 1074,224 1107,215 1148,205" '
            f'fill="none" stroke="{palette.amber}" stroke-width="2" stroke-dasharray="5 4"/>'
        ),
        _text(828, 310, "D+00", "mono small", fill=palette.muted),
        _text(975, 310, "FORECAST", "mono small", fill=palette.amber, anchor="middle"),
        _text(1150, 310, "D+65", "mono small", fill=palette.muted, anchor="end"),
        _text(
            1170,
            338,
            "not demos // systems that had to work",
            "mono small",
            fill=palette.muted,
            anchor="end",
        ),
        "</svg>",
    ])
    return "\n".join(lines) + "\n"
