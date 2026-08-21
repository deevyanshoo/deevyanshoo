from __future__ import annotations

from .svg import Palette, Theme, frame, text


WIDTH = 1200
HEIGHT = 420


def _dag(colors: Palette) -> list[str]:
    nodes = ((55, 218), (116, 178), (118, 272), (188, 214), (252, 166), (258, 270))
    edges = ((0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (3, 4), (3, 5), (4, 5))
    lines = [
        '<g data-system="dag" data-module-width="280">',
        text(24, 84, "DAG LEDGER", "sans system-title", colors.ink),
        text(24, 108, "alternative consensus experiment", "sans system-subtitle", colors.secondary),
        text(24, 139, "crawler / network logic", "mono fact", colors.cyan),
        text(24, 157, "peer approvals + validation incentives", "mono fact", colors.muted),
    ]
    for left, right in edges:
        x1, y1 = nodes[left]
        x2, y2 = nodes[right]
        lines.append(
            f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{colors.line}" '
            'stroke-width="1.5" marker-end="url(#arrow)"/>'
        )
    for index, (x, y) in enumerate(nodes):
        color = colors.amber if index < 3 else colors.cyan
        lines.extend(
            (
                f'<circle cx="{x}" cy="{y}" r="10" fill="{colors.background}" '
                f'stroke="{color}" stroke-width="1.5"/>',
                f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>',
            )
        )
    lines.extend(
        (
            text(24, 326, "DAG, not a linear chain.", "sans note", colors.secondary),
            text(24, 346, "Exploring alternatives to linear-chain growth.", "sans note", colors.muted),
            "</g>",
        )
    )
    return lines


def _aviation(colors: Palette) -> list[str]:
    history = "340,279 370,266 400,270 430,245 460,253 490,232 520,242 550,218"
    forecast = "550,218 580,205 610,194 646,177"
    return [
        '<g data-system="aviation" data-module-width="334">',
        text(330, 84, "AVIATION FORECASTING", "sans system-title", colors.ink),
        text(330, 108, "demand forecasting 65 days ahead", "sans system-subtitle", colors.secondary),
        text(330, 151, ">90% accuracy", "sans evidence", colors.amber),
        text(520, 151, "~800 TB/day", "sans evidence", colors.ink),
        text(330, 170, "forecast", "mono fact", colors.muted),
        text(520, 170, "data environment", "mono fact", colors.muted),
        f'<path d="M330 290H650" stroke="{colors.line}"/>',
        f'<path d="M550 190V306" stroke="{colors.line}" stroke-dasharray="4 5"/>',
        f'<polyline points="{history}" fill="none" stroke="{colors.secondary}" stroke-width="2"/>',
        f'<polyline points="{forecast}" fill="none" stroke="{colors.amber}" stroke-width="2" stroke-dasharray="5 4"/>',
        text(330, 311, "HISTORY", "mono fact", colors.muted),
        text(550, 311, "NOW", "mono fact", colors.amber, anchor="middle"),
        text(650, 311, "D+65", "mono fact", colors.muted, anchor="end"),
        text(330, 346, "Large-scale ML systems that had to work.", "sans note", colors.secondary),
        "</g>",
    ]


def _jarvis(colors: Palette) -> list[str]:
    return [
        '<g data-system="jarvis" data-module-width="486">',
        text(690, 84, "JARVIS", "sans system-title jarvis-title", colors.ink),
        text(690, 110, "mobile-first personal AI", "sans system-subtitle", colors.secondary),
        text(690, 139, "A real assistant living on my phone.", "sans note", colors.muted),
        f'<rect x="704" y="183" width="66" height="118" rx="13" fill="{colors.surface}" '
        f'stroke="{colors.secondary}" stroke-width="1.5"/>',
        f'<path d="M725 194H749" stroke="{colors.line}" stroke-width="2"/>',
        f'<circle cx="737" cy="282" r="4" fill="{colors.amber}"/>',
        text(737, 246, "J", "sans evidence", colors.ink, anchor="middle"),
        f'<path d="M770 241H821" stroke="{colors.line}" marker-end="url(#arrow)"/>',
        f'<rect x="827" y="211" width="112" height="60" rx="7" fill="{colors.background}" '
        f'stroke="{colors.amber}" stroke-width="1.5"/>',
        text(883, 237, "INFERENCE", "mono fact", colors.amber, anchor="middle"),
        text(883, 255, "ROUTER", "mono fact", colors.secondary, anchor="middle"),
        f'<path d="M939 230L989 194" stroke="{colors.line}" marker-end="url(#arrow)"/>',
        f'<path d="M939 252L989 288" stroke="{colors.line}" marker-end="url(#arrow)"/>',
        f'<rect x="996" y="164" width="170" height="62" rx="7" fill="{colors.surface}" '
        f'stroke="{colors.cyan}" stroke-width="1.5"/>',
        text(1012, 190, "ON DEVICE", "mono fact", colors.cyan),
        text(1012, 211, "quantized local SLM", "sans note", colors.secondary),
        f'<rect x="996" y="258" width="170" height="62" rx="7" fill="{colors.surface}" '
        f'stroke="{colors.muted}" stroke-width="1.5"/>',
        text(1012, 284, "WHEN NEEDED", "mono fact", colors.muted),
        text(1012, 305, "cloud LLM", "sans note", colors.secondary),
        text(690, 346, "privacy \u00b7 latency \u00b7 capability", "mono jarvis-principles", colors.cyan),
        "</g>",
    ]


def render_systems_panel(theme: Theme, *, build_id: str = "dev") -> str:
    lines, colors = frame(
        theme,
        WIDTH,
        HEIGHT,
        "Things I built because I could",
        (
            "A DAG ledger, aviation forecasting at scale, and Jarvis: "
            "distributed systems to large-scale ML to edge AI."
        ),
        build_id=build_id,
    )
    lines.extend(
        (
            "<style>",
            ".section-title{font-size:13px;font-weight:760;letter-spacing:1.4px}",
            ".progression{font-size:10px;letter-spacing:.65px}",
            ".system-title{font-size:22px;font-weight:790;letter-spacing:-.35px}",
            ".jarvis-title{font-size:27px}",
            ".system-subtitle{font-size:14px;font-weight:560}",
            ".evidence{font-size:24px;font-weight:780;letter-spacing:-.5px}",
            ".fact{font-size:10px;letter-spacing:.55px}",
            ".note{font-size:12px}",
            ".jarvis-principles{font-size:11px;font-weight:700;letter-spacing:.8px}",
            "</style>",
            "<defs>",
            (
                '<marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" '
                'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                f'<path d="M0 0L8 4L0 8Z" fill="{colors.muted}"/>'
                "</marker>"
            ),
            "</defs>",
            f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{colors.background}"/>',
            (
                f'<rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" '
                f'rx="17" fill="none" stroke="{colors.line}"/>'
            ),
            text(24, 30, "THINGS I BUILT BECAUSE I COULD", "sans section-title", colors.amber),
            text(
                1176,
                30,
                "DISTRIBUTED SYSTEMS  \u2192  LARGE-SCALE ML  \u2192  EDGE AI",
                "mono progression",
                colors.muted,
                anchor="end",
            ),
            f'<path d="M24 48H1176" stroke="{colors.line}"/>',
            f'<path d="M306 64V372" stroke="{colors.line}"/>',
            f'<path d="M670 64V372" stroke="{colors.line}"/>',
        )
    )
    lines.extend(_dag(colors))
    lines.extend(_aviation(colors))
    lines.extend(_jarvis(colors))
    lines.extend(
        (
            f'<path d="M24 372H1176" stroke="{colors.line}"/>',
            text(24, 398, "BUILT TO LEARN. KEPT BECAUSE THEY TAUGHT ME SOMETHING.", "mono progression", colors.muted),
            "</svg>",
        )
    )
    return "\n".join(lines) + "\n"
