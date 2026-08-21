# Maintaining the profile

The committed renderer uses only Python 3.13. Portrait regeneration and its tests use
the pinned optional Pillow dependency:

```bash
python -m pip install ".[portrait]"
```

## Local verification

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/generate.py --offline
python -m compileall -q src scripts tests
```

Run the generator twice when changing the renderer. The second run must report `profile assets unchanged`.

## Live telemetry

Scheduled generation first reads the optional `PROFILE_TOKEN` repository secret and otherwise falls back to `github.token`. To include private/internal contributions in anonymous totals, enable private contribution counts on the GitHub profile, create a classic personal access token with only the `read:user` scope, and save it as `PROFILE_TOKEN` in this repository. It needs no repository access and cannot read private repository names, metadata, or contents.

The telemetry query requests counts only. Do not add repository identity fields—even temporarily—to the query, fixtures, logs, models, or renderer. Tests use a clearly synthetic sensitive-data sentinel to prove unexpected values are discarded before rendering.

## Design edits

Public copy lives in `src/operator_profile/content.py`; hero and systems geometry live
in `hero.py` and `systems.py`; themes and escaping live in `svg.py`; GitHub API
handling lives in `telemetry.py`. The four committed SVGs include a fingerprint of
every renderer input, and tests fail when those assets are stale.

The portrait source photo is deliberately not part of the repository. To rebuild the
four-tone vector data, pass a local source explicitly:

```bash
python scripts/build_portrait.py --source /path/to/photo.jpg --output src/operator_profile/portrait_data.py
```

Never add the source photograph to Git. Keep the content and telemetry boundaries
separate so a design edit cannot weaken the aggregate-only data contract.
