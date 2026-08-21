from __future__ import annotations

from .hero import render_hero
from .model import ProfileData
from .svg import Theme


def render_profile(
    data: ProfileData,
    theme: Theme,
    *,
    status_label: str = "LIVE",
    build_id: str = "dev",
) -> str:
    return render_hero(
        data,
        theme,
        status_label=status_label,
        build_id=build_id,
    )


def render_systems(theme: Theme, *, build_id: str = "dev") -> str:
    from .systems import render_systems_panel

    return render_systems_panel(theme, build_id=build_id)
