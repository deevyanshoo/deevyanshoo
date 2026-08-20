from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .model import GitHubStats


GRAPHQL_ENDPOINT = "https://api.github.com/graphql"

# Privacy is enforced at the query boundary: only counts and public-star totals
# are requested. No repository identity fields are part of this document.
PRIVATE_SAFE_QUERY = """
query ProfileAggregates($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions }
      restrictedContributionsCount
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
    }
    pullRequests(states: MERGED) { totalCount }
    repositories(first: 100, privacy: PUBLIC, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    repositoriesContributedTo(
      first: 1
      includeUserRepositories: true
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, PULL_REQUEST_REVIEW]
    ) { totalCount }
  }
}
""".strip()


def _mapping(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"GitHub GraphQL response is missing {context}")
    return value


def _count(value: object, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"GitHub GraphQL returned an invalid {context}")
    return value


def parse_stats(payload: Mapping[str, Any]) -> GitHubStats:
    """Reduce a GraphQL payload immediately to anonymous scalar aggregates."""
    if payload.get("errors"):
        raise ValueError("GitHub GraphQL returned one or more errors")

    data = _mapping(payload.get("data"), "data")
    user = _mapping(data.get("user"), "user")
    contributions = _mapping(
        user.get("contributionsCollection"), "contributionsCollection"
    )
    calendar = _mapping(contributions.get("contributionCalendar"), "calendar")
    pull_requests = _mapping(user.get("pullRequests"), "pullRequests")
    repositories = _mapping(user.get("repositories"), "repositories")
    contributed = _mapping(
        user.get("repositoriesContributedTo"), "repositoriesContributedTo"
    )

    nodes = repositories.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("GitHub GraphQL response is missing public star totals")

    stars = 0
    for node in nodes:
        public_repo = _mapping(node, "public repository aggregate")
        stars += _count(public_repo.get("stargazerCount"), "stargazerCount")

    return GitHubStats(
        contributions_ytd=_count(calendar.get("totalContributions"), "contributions"),
        private_contributions_ytd=_count(
            contributions.get("restrictedContributionsCount"),
            "restricted contributions",
        ),
        commit_contributions_ytd=_count(
            contributions.get("totalCommitContributions"), "commit contributions"
        ),
        pull_request_contributions_ytd=_count(
            contributions.get("totalPullRequestContributions"),
            "pull request contributions",
        ),
        issue_contributions_ytd=_count(
            contributions.get("totalIssueContributions"), "issue contributions"
        ),
        review_contributions_ytd=_count(
            contributions.get("totalPullRequestReviewContributions"),
            "review contributions",
        ),
        merged_pull_requests=_count(pull_requests.get("totalCount"), "merged PRs"),
        public_repositories=_count(repositories.get("totalCount"), "public repos"),
        repositories_contributed_to=_count(
            contributed.get("totalCount"), "repositories contributed to"
        ),
        stars_earned=stars,
    )


def fetch_stats(
    token: str,
    login: str = "deevyanshoo",
    now: datetime | None = None,
    timeout_seconds: float = 20.0,
) -> GitHubStats:
    if not token.strip():
        raise ValueError("a GitHub token is required for live telemetry")

    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    moment = moment.astimezone(timezone.utc)
    year_start = datetime(moment.year, 1, 1, tzinfo=timezone.utc)

    body = json.dumps(
        {
            "query": PRIVATE_SAFE_QUERY,
            "variables": {
                "login": login,
                "from": year_start.isoformat().replace("+00:00", "Z"),
                "to": moment.isoformat().replace("+00:00", "Z"),
            },
        },
        separators=(",", ":"),
    ).encode("utf-8")
    request = Request(
        GRAPHQL_ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "deevyanshoo-profile/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"GitHub telemetry request failed with HTTP {error.code}") from error
    except URLError as error:
        raise RuntimeError("GitHub telemetry request could not reach GitHub") from error

    if not isinstance(payload, Mapping):
        raise ValueError("GitHub GraphQL returned a non-object response")
    return parse_stats(payload)
