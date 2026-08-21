from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from operator_profile.model import ProfileData  # noqa: E402
from operator_profile.render import render_profile, render_systems  # noqa: E402
from operator_profile.telemetry import fetch_stats, parse_stats  # noqa: E402


def _load_fixture(path: Path) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("offline fixture must contain a JSON object")
    return payload


def _write_if_changed(destination: Path, content: str) -> bool:
    encoded = content.encode("utf-8")
    if destination.exists() and destination.read_bytes() == encoded:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_bytes(encoded)
    temporary.replace(destination)
    return True


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic light/dark GitHub profile SVGs."
    )
    parser.add_argument("--offline", action="store_true", help="use aggregate fixture data")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=ROOT / "data" / "fallback-stats.json",
    )
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    parser.add_argument("--login", default="deevyanshoo")
    return parser.parse_args()


def main() -> int:
    arguments = _arguments()
    if arguments.offline:
        stats = parse_stats(_load_fixture(arguments.fixture))
    else:
        token = (
            os.environ.get("PROFILE_TOKEN", "").strip()
            or os.environ.get("GITHUB_TOKEN", "").strip()
        )
        if not token:
            raise SystemExit(
                "Live generation needs PROFILE_TOKEN or GITHUB_TOKEN; use --offline locally."
            )
        stats = fetch_stats(token=token, login=arguments.login)

    data = ProfileData(stats=stats)
    changed: list[str] = []
    for theme in ("light", "dark"):
        profile_destination = arguments.output_dir / f"profile-{theme}.svg"
        if _write_if_changed(profile_destination, render_profile(data, theme)):
            changed.append(profile_destination.name)

        systems_destination = arguments.output_dir / f"systems-{theme}.svg"
        if _write_if_changed(systems_destination, render_systems(theme)):
            changed.append(systems_destination.name)

    print("updated: " + ", ".join(changed) if changed else "profile assets unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
