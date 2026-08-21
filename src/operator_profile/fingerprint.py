from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Iterable


SOURCE_INPUTS = (
    "src/operator_profile/content.py",
    "src/operator_profile/model.py",
    "src/operator_profile/svg.py",
    "src/operator_profile/portrait.py",
    "src/operator_profile/portrait_data.py",
    "src/operator_profile/hero.py",
    "src/operator_profile/systems.py",
    "src/operator_profile/render.py",
    "src/operator_profile/telemetry.py",
    "scripts/generate.py",
)


def source_fingerprint(
    root: Path,
    inputs: Iterable[str] = SOURCE_INPUTS,
) -> str:
    digest = sha256()
    for relative in inputs:
        path = root / relative
        payload = path.read_bytes()
        encoded_name = relative.replace("\\", "/").encode("utf-8")
        digest.update(len(encoded_name).to_bytes(4, "big"))
        digest.update(encoded_name)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()[:12]
