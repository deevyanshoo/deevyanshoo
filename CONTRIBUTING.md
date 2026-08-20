# Maintaining the profile

The profile is intentionally dependency-free. Python 3.13 is the only runtime requirement.

## Local verification

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/generate.py --offline
python -m compileall -q src scripts tests
```

Run the generator twice when changing the renderer. The second run must report `profile assets unchanged`.

## Live telemetry

Scheduled generation first reads the optional `PROFILE_TOKEN` repository secret and otherwise falls back to `github.token`. For aggregate private contribution visibility, create a fine-grained personal access token owned by `deevyanshoo`, grant read-only repository metadata to only the repositories whose activity may be counted, and save it as `PROFILE_TOKEN` in this repository.

The telemetry query requests counts only. Do not add repository identity fields—even temporarily—to the query, fixtures, logs, models, or renderer.

## Design edits

Public copy lives in `src/operator_profile/content.py`, portrait rows in `portrait.py`, themes/layout in `render.py`, and GitHub API handling in `telemetry.py`. Keep those boundaries intact so content changes cannot weaken the privacy boundary.
