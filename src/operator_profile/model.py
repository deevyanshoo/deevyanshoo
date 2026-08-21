from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class GitHubStats:
    contributions_ytd: int
    restricted_contributions_ytd: int

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{field.name} must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class ProfileData:
    stats: GitHubStats
