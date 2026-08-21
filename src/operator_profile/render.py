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
    bg: str
    panel: str
    border: str
    primary: str
    secondary: str
    muted: str
    amber: str
    cyan: str
    green: str
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
    fill: str,
    *,
    anchor: str | None = None,
    opacity: float | None = None,
) -> str:
    attrs = [f'class="{css_class}"', f'fill="{fill}"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'<text x="{x}" y="{y}" {" ".join(attrs)}>{escape(value, quote=True)}</text>'


def _frame(theme: Theme, width: int, height: int, title: str, desc: str) -> tuple[list[str], Palette]:
    if theme not in PALETTES:
        raise ValueError("theme must be 'light' or 'dark'")
    p = PALETTES[theme]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" data-theme="{theme}">',
        f'<title>{escape(title)}</title>',
        f'<desc>{escape(desc)}</desc>',
        '<defs>',
        f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p.grid}" stroke-width="1"/></pattern>',
        f'<linearGradient id="pulse" x1="0" x2="1"><stop stop-color="{p.amber}"/><stop offset="1" stop-color="{p.cyan}"/></linearGradient>',
        '</defs>',
        '<style>',
        ".sans{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Arial,sans-serif}",
        ".mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace}",
        '.name{font-size:48px;font-weight:800;letter-spacing:-1.4px}',
        '.role{font-size:14px;font-weight:700;letter-spacing:1.6px}',
        '.eyebrow{font-size:13px;font-weight:700;letter-spacing:1.8px}',
        '.tag{font-size:25px;font-weight:700;letter-spacing:-.4px}',
        '.body{font-size:15px}',
        '.small{font-size:12px}',
        '.micro{font-size:11px;letter-spacing:.7px}',
        '.portrait{font-size:13px;font-weight:700;white-space:pre}',
        '.mission{font-size:28px;font-weight:800}',
        '.card-title{font-size:22px;font-weight:800}',
        '.metric{font-size:24px;font-weight:800}',
        '</style>',
        f'<rect width="{width}" height="{height}" rx="18" fill="{p.bg}"/>',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" fill="{p.panel}" stroke="{p.border}"/>',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" fill="url(#grid)" opacity=".45"/>',
    ]
    return lines, p


def render_profile(data: ProfileData, theme: Theme, *, status_label: str = "LIVE") -> str:
    lines, p = _frame(
        theme,
        1200,
        520,
        "Divyanshu Goyal — AI architect, founder, builder",
        "Image-derived ASCII portrait, Nnomi current mission, AI systems focus, and aggregate GitHub activity.",
    )
    stats = data.stats

    lines.extend([
        f'<line x1="28" y1="54" x2="1172" y2="54" stroke="{p.border}"/>',
        _text(30, 35, "deevyanshoo@operator", "mono eyebrow", p.muted),
        f'<circle cx="990" cy="31" r="4" fill="{p.green}"/>',
        _text(1004, 35, f"{status_label} // {stats.contributions_ytd:,} CONTRIBUTIONS YTD", "mono micro", p.muted),
        f'<line x1="432" y1="76" x2="432" y2="458" stroke="{p.border}"/>',
        _text(30, 84, "PORTRAIT // ASCII SCAN", "mono eyebrow", p.cyan),
    ])

    y = 108
    for row in PORTRAIT:
        lines.append(_text(30, y, row, "mono portrait", p.secondary, opacity=0.82))
        y += 13

    lines.extend([
        _text(30, 476, "image-derived // approved portrait", "mono micro", p.muted),
        _text(470, 86, "IDENTITY // 00", "mono eyebrow", p.cyan),
        _text(470, 137, NAME, "sans name", p.primary),
        _text(470, 169, ROLE, "mono role", p.amber),
        _text(470, 218, TAGLINE, "sans tag", p.primary),
        _text(470, 246, POSITIONING, "sans body", p.secondary),
        f'<line x1="470" y1="274" x2="1168" y2="274" stroke="{p.border}"/>',
        _text(470, 302, f"CURRENT MISSION // {CURRENT_MISSION}", "mono eyebrow", p.amber),
        _text(470, 338, CURRENT_MISSION, "sans mission", p.primary),
        _text(590, 336, CURRENT_MISSION_URL, "mono small", p.cyan),
        _text(470, 365, CURRENT_MISSION_LINE_1, "sans body", p.secondary),
        _text(470, 387, CURRENT_MISSION_LINE_2, "sans body", p.secondary),
    ])

    journey = (("EARN", 490), ("SPEND", 625), ("PROTECT", 770), ("INVEST", 930), ("WEALTH", 1080))
    for i, (label, x) in enumerate(journey):
        if i < len(journey) - 1:
            lines.append(f'<line x1="{x}" y1="414" x2="{journey[i + 1][1]}" y2="414" stroke="url(#pulse)" stroke-width="2" opacity=".72"/>')
        dot = p.amber if i < 3 else p.cyan
        lines.append(f'<circle cx="{x}" cy="414" r="5" fill="{dot}"/>')
        lines.append(_text(x, 436, label, "mono micro", p.muted, anchor="middle"))

    lines.extend([
        _text(470, 462, f"also building // {SECONDARY_MISSION}", "mono micro", p.secondary),
        f'<line x1="28" y1="490" x2="1172" y2="490" stroke="{p.border}"/>',
        _text(30, 510, LOCATION, "mono micro", p.muted),
        _text(220, 510, "MSE // PENN", "mono micro", p.muted),
        _text(350, 510, "AI ARCHITECT @ ZS", "mono micro", p.muted),
        _text(540, 510, "runtime v26", "mono micro", p.muted),
        _text(690, 510, "inference local > cloud", "mono micro", p.muted),
        _text(930, 510, "garage_target 911", "mono micro", p.amber),
        '</svg>',
    ])
    return "\n".join(lines) + "\n"


def render_systems(theme: Theme) -> str:
    lines, p = _frame(
        theme,
        1200,
        360,
        "Things I built because I could",
        "JARVIS hybrid inference, a DAG ledger, and large-scale aviation forecasting.",
    )
    lines.extend([
        _text(28, 36, "THINGS I BUILT BECAUSE I COULD // 02", "mono eyebrow", p.amber),
        _text(1170, 36, "distributed systems  >  large-scale ML  >  edge AI", "mono small", p.muted, anchor="end"),
        f'<line x1="28" y1="54" x2="1172" y2="54" stroke="{p.border}"/>',
        f'<line x1="400" y1="78" x2="400" y2="316" stroke="{p.border}"/>',
        f'<line x1="800" y1="78" x2="800" y2="316" stroke="{p.border}"/>',
        _text(28, 88, "01 // JARVIS", "mono eyebrow", p.cyan),
        _text(28, 120, "HYBRID AI", "sans card-title", p.primary),
        _text(28, 146, "personal assistant on a phone", "sans body", p.secondary),
        f'<rect x="44" y="178" width="74" height="102" rx="12" fill="none" stroke="{p.secondary}" stroke-width="2"/>',
        f'<rect x="155" y="205" width="82" height="46" rx="8" fill="none" stroke="{p.amber}" stroke-width="1.5"/>',
        _text(196, 232, "ROUTER", "mono small", p.amber, anchor="middle"),
        f'<line x1="118" y1="229" x2="155" y2="229" stroke="{p.muted}"/>',
        f'<line x1="237" y1="217" x2="290" y2="190" stroke="{p.amber}"/>',
        f'<line x1="237" y1="239" x2="290" y2="265" stroke="{p.cyan}"/>',
        f'<rect x="290" y="168" width="82" height="45" rx="7" fill="none" stroke="{p.amber}"/>',
        _text(331, 188, "LOCAL", "mono small", p.amber, anchor="middle"),
        _text(331, 204, "SLM", "mono small", p.secondary, anchor="middle"),
        f'<rect x="290" y="244" width="82" height="45" rx="7" fill="none" stroke="{p.cyan}"/>',
        _text(331, 264, "CLOUD", "mono small", p.cyan, anchor="middle"),
        _text(331, 280, "LLM", "mono small", p.secondary, anchor="middle"),
        _text(28, 318, "privacy HIGH // latency LOW // cloud optional", "mono small", p.muted),
        _text(428, 88, "02 // DAG LEDGER", "mono eyebrow", p.cyan),
        _text(428, 120, "DISTRIBUTED SYSTEMS", "sans card-title", p.primary),
        _text(428, 146, "peer-approved blocks without a linear chain", "sans body", p.secondary),
    ])

    nodes = {"a": (475, 205), "b": (560, 176), "c": (645, 210), "d": (535, 265), "e": (690, 270), "f": (745, 188)}
    edges = (("a", "b"), ("a", "d"), ("b", "c"), ("b", "d"), ("c", "d"), ("c", "f"), ("c", "e"), ("d", "e"), ("f", "e"))
    for left, right in edges:
        x1, y1 = nodes[left]
        x2, y2 = nodes[right]
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{p.muted}" stroke-width="1.5" opacity=".75"/>')
    for i, (_, (x, y)) in enumerate(nodes.items()):
        color = p.amber if i in (0, 1, 3) else p.cyan
        lines.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{p.panel}" stroke="{color}" stroke-width="2"/>')
        lines.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')

    lines.extend([
        _text(428, 318, "DAG growth // P2P approvals // custom consensus", "mono small", p.muted),
        _text(828, 88, "03 // AVIATION", "mono eyebrow", p.cyan),
        _text(828, 120, "FORECASTING AT SCALE", "sans card-title", p.primary),
        _text(828, 146, "demand prediction 65 days ahead", "sans body", p.secondary),
        _text(828, 200, ">90%", "sans metric", p.amber),
        _text(910, 198, "forecast accuracy", "mono small", p.muted),
        _text(828, 238, "~800 TB/day", "sans metric", p.primary),
        _text(970, 236, "data environment", "mono small", p.muted),
        f'<line x1="828" y1="285" x2="1150" y2="285" stroke="{p.border}"/>',
        f'<line x1="975" y1="260" x2="975" y2="306" stroke="{p.border}" stroke-dasharray="4 4"/>',
        f'<polyline points="828,287 860,272 892,279 924,248 956,259 988,240 1020,246 1052,220 1084,229 1116,208 1148,214" fill="none" stroke="{p.secondary}" stroke-width="2"/>',
        f'<polyline points="975,257 1008,246 1041,236 1074,224 1107,215 1148,205" fill="none" stroke="{p.amber}" stroke-width="2" stroke-dasharray="5 4"/>',
        _text(828, 310, "D+00", "mono small", p.muted),
        _text(975, 310, "FORECAST", "mono small", p.amber, anchor="middle"),
        _text(1150, 310, "D+65", "mono small", p.muted, anchor="end"),
        _text(1170, 338, "not demos // systems that had to work", "mono small", p.muted, anchor="end"),
        '</svg>',
    ])
    return "\n".join(lines) + "\n"
