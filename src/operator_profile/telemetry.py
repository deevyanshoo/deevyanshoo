from __future__ import annotations

import json
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
) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions }
      restrictedContributionsCount
    }
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


def parse_stats(payload: Mapping[str, Any]) -> GitHubStats:
    """Reduce one GraphQL page immediately to anonymous scalar aggregates."""
    user = _user(payload)
    contributions = _mapping(
        user.get("contributionsCollection"), "contributionsCollection"
    )
    calendar = _mapping(contributions.get("contributionCalendar"), "calendar")
    return GitHubStats(
        contributions_ytd=_count(calendar.get("totalContributions"), "contributions"),
        restricted_contributions_ytd=_count(
            contributions.get("restrictedContributionsCount"),
            "restricted contributions",
        ),
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

    variables: Mapping[str, Any] = {
        "login": login,
        "from": year_start.isoformat().replace("+00:00", "Z"),
        "to": moment.isoformat().replace("+00:00", "Z"),
    }
    return parse_stats(request_page(token, variables, timeout_seconds))
