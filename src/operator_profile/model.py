from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class GitHubStats:
    contributions_ytd: int
    private_contributions_ytd: int
    commit_contributions_ytd: int
    pull_request_contributions_ytd: int
    issue_contributions_ytd: int
    review_contributions_ytd: int
    merged_pull_requests: int
    public_repositories: int
    repositories_contributed_to: int
    stars_earned: int

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{field.name} must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class ProfileData:
    stats: GitHubStats
    private_activity_aggregated: bool

    def __post_init__(self) -> None:
        if not isinstance(self.private_activity_aggregated, bool):
            raise ValueError("private_activity_aggregated must be a boolean")
