"""Deterministic, privacy-safe GitHub profile renderer."""

from typing import Any

from .model import GitHubStats, ProfileData


def render_profile(*args: Any, **kwargs: Any) -> str:
    """Render the profile without eagerly importing the visual modules."""
    from .render import render_profile as _render_profile

    return _render_profile(*args, **kwargs)

__all__ = ["GitHubStats", "ProfileData", "render_profile"]
