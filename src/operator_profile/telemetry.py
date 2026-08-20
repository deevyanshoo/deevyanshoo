from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .model import GitHubStats


GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
Transport = Callable[[str, Mapping[str, Any], float], Mapping[str, Any]]

# Privacy is enforced at the query boundary. Repository identity fields are
# absent; the only per-repository value requested is a public star count.
PRIVATE_SAFE_QUERY = """
query ProfileAggregates(
  $login: String!
  $from: DateTime!
  $to: DateTime!
  $cursor: String
) {
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
    publicRepositories: repositories(first: 1, privacy: PUBLIC) { totalCount }
    starredRepositories: repositories(
      first: 100
      after: $cursor
      privacy: PUBLIC
      isFork: false
    ) {
      nodes { stargazerCount }
      pageInfo { hasNextPage endCursor }
    }
    recentRepositories: repositoriesContributedTo(
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


def _user(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("errors"):
        raise ValueError("GitHub GraphQL returned one or more errors")
    return _mapping(_mapping(payload.get("data"), "data").get("user"), "user")


def _star_page(user: Mapping[str, Any]) -> tuple[int, bool, str | None]:
    repositories = _mapping(user.get("starredRepositories"), "starredRepositories")
    nodes = repositories.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("GitHub GraphQL response is missing public star totals")
    stars = sum(
        _count(_mapping(node, "public repository aggregate").get("stargazerCount"), "stars")
        for node in nodes
    )
    page_info = _mapping(repositories.get("pageInfo"), "star pageInfo")
    has_next = page_info.get("hasNextPage")
    cursor = page_info.get("endCursor")
    if not isinstance(has_next, bool):
        raise ValueError("GitHub GraphQL returned invalid star pagination state")
    if cursor is not None and not isinstance(cursor, str):
        raise ValueError("GitHub GraphQL returned an invalid star cursor")
    if has_next and not cursor:
        raise ValueError("GitHub GraphQL omitted the next star cursor")
    return stars, has_next, cursor


def parse_stats(payload: Mapping[str, Any]) -> GitHubStats:
    """Reduce one GraphQL page immediately to anonymous scalar aggregates."""
    user = _user(payload)
    contributions = _mapping(
        user.get("contributionsCollection"), "contributionsCollection"
    )
    calendar = _mapping(contributions.get("contributionCalendar"), "calendar")
    pull_requests = _mapping(user.get("pullRequests"), "pullRequests")
    public_repositories = _mapping(
        user.get("publicRepositories"), "publicRepositories"
    )
    recent_repositories = _mapping(
        user.get("recentRepositories"), "recentRepositories"
    )
    stars, _, _ = _star_page(user)

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
        public_repositories=_count(
            public_repositories.get("totalCount"), "public repos"
        ),
        repositories_contributed_to=_count(
            recent_repositories.get("totalCount"), "recent repositories"
        ),
        stars_earned=stars,
    )


def _post_graphql(
    token: str,
    variables: Mapping[str, Any],
    timeout_seconds: float,
) -> Mapping[str, Any]:
    body = json.dumps(
        {"query": PRIVATE_SAFE_QUERY, "variables": variables},
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
    return payload


def fetch_stats(
    token: str,
    login: str = "deevyanshoo",
    now: datetime | None = None,
    timeout_seconds: float = 20.0,
    transport: Transport | None = None,
) -> GitHubStats:
    if not token.strip():
        raise ValueError("a GitHub token is required for live telemetry")

    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    moment = moment.astimezone(timezone.utc)
    year_start = datetime(moment.year, 1, 1, tzinfo=timezone.utc)
    request_page = transport or _post_graphql

    cursor: str | None = None
    seen_cursors: set[str] = set()
    total_stars = 0
    aggregate: GitHubStats | None = None
    while True:
        variables: Mapping[str, Any] = {
            "login": login,
            "from": year_start.isoformat().replace("+00:00", "Z"),
            "to": moment.isoformat().replace("+00:00", "Z"),
            "cursor": cursor,
        }
        payload = request_page(token, variables, timeout_seconds)
        user = _user(payload)
        page_stars, has_next, next_cursor = _star_page(user)
        total_stars += page_stars
        if aggregate is None:
            aggregate = parse_stats(payload)
        if not has_next:
            return replace(aggregate, stars_earned=total_stars)
        if next_cursor in seen_cursors:
            raise ValueError("GitHub GraphQL repeated a star pagination cursor")
        seen_cursors.add(next_cursor)
        cursor = next_cursor
