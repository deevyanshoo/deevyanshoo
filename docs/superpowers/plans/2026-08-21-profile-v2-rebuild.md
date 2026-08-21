# GitHub Profile V2 Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the rejected GitHub profile with a memorable theme-aware operator field note centered on Divyanshu’s portrait, AI systems, and Nnomi.

**Architecture:** Keep the dependency-light Python generator and frozen telemetry model. Split SVG primitives, portrait data, hero layout, and systems layout into focused modules behind the existing `render_profile` and `render_systems` API. Commit deterministic vector portrait data and use a source fingerprint to detect stale generated assets without comparing live telemetry to offline fixtures.

**Tech Stack:** Python 3.13, standard-library SVG/XML generation, optional Pillow portrait tool, unittest, GitHub Actions, headless Microsoft Edge for local visual QA.

## Global Constraints

- Develop only on `profile-v2-rebuild` in `C:\Users\Divyanshu\deevyanshoo-profile-v2` until all gates pass.
- Hero: 1200 × 560. Systems: 1200 × 420. Inspect both themes at 1200 px and 880 px.
- Public identity must include `Divyanshu Goyal`, `AI Architect`, founder/builder identity, `making large models fit small boxes`, `Nnomi`, `Gurugram ↔ wherever`, and all four approved easter eggs.
- The original portrait photograph is never committed.
- Only year-to-date contributions may render, and only at 100 or more.
- No private repository identity or metadata may enter the query, model, logs, fixtures, renderer, or committed SVG.
- Public output must exclude `approved portrait`, `approved desk portrait`, `image-derived`, `source portrait`, and `privacy mode`.
- Keep `actions/checkout@v7` and `actions/setup-python@v7` with least privilege.

## File structure

- `src/operator_profile/content.py`: typed public copy and system facts.
- `src/operator_profile/model.py`: minimal frozen aggregate telemetry.
- `src/operator_profile/svg.py`: palette, escaping, frame, and SVG primitives.
- `src/operator_profile/portrait_data.py`: generated four-tone run data only.
- `src/operator_profile/portrait.py`: portrait SVG composition.
- `src/operator_profile/hero.py`: hero geometry and thresholded telemetry.
- `src/operator_profile/systems.py`: three-system visual narrative.
- `src/operator_profile/render.py`: stable public facade.
- `src/operator_profile/fingerprint.py`: deterministic source fingerprint.
- `scripts/build_portrait.py`: explicit-source optional Pillow pipeline.
- `scripts/generate.py`: atomic generation for all four assets.
- `tests/`: behavior, privacy, freshness, README, and workflow contracts.
- `docs/design-review/profile-v2-qa.md`: recorded visual iterations and supervisor findings.

---

### Task 1: Replace the public contract with V2 expectations

**Files:** `tests/test_render.py`, `tests/test_repository_contract.py`.

**Interface:** Preserve `render_profile(ProfileData, Theme)` and `render_systems(Theme)`.

- [ ] Write assertions for the V2 identity, Nnomi hierarchy/journey, precise system facts, Unicode arrow, README order, forbidden phrases, vanity metrics, stale store status, and fake-terminal numbering.
- [ ] Run `$env:PYTHONPATH='src'; python -m unittest tests.test_render tests.test_repository_contract -v`; expect V2 contract failures.
- [ ] Commit only the failing tests as `test: define profile v2 public contract`.

### Task 2: Minimize telemetry at the privacy boundary

**Files:** `tests/test_telemetry.py`, `model.py`, `telemetry.py`, and both JSON fixtures.

**Interface:** `GitHubStats(contributions_ytd, restricted_contributions_ytd)`; `parse_stats(payload)`; `fetch_stats(...)`.

- [ ] Test that the query requests only total and restricted contribution aggregates and rejects nodes plus repository, PR, organization, name, description, topic, URL, branch, issue, commit, and file fields.
- [ ] Run telemetry tests; expect the old query/model to fail.
- [ ] Reduce the frozen model/parser, remove star/repository logic, preserve injected transport, UTC bounds, validation, and fail-closed errors.
- [ ] Shrink fixtures, rerun GREEN, and commit `refactor: minimize profile telemetry boundary`.

### Task 3: Add SVG primitives and source fingerprinting

**Files:** New `svg.py` and `fingerprint.py`; render/generator tests.

**Interfaces:** `Palette`, `palette(theme)`, `text(...)`, `frame(...)`, `source_fingerprint(root)`, `SOURCE_INPUTS`.

- [ ] Test theme rejection, XML escaping, independent palettes, stable fingerprints, and input-sensitive digests.
- [ ] Run tests RED for missing modules.
- [ ] Implement system-sans display, mono annotations, centralized escaping, and a 12-hex length-delimited SHA-256.
- [ ] Rerun GREEN and commit `feat: add profile svg foundation`.

### Task 4: Build the deterministic portrait treatment

**Files:** `pyproject.toml`, new `scripts/build_portrait.py`, `portrait_data.py`, `tests/test_portrait.py`, replacement `portrait.py`.

**Interfaces:** `quantize_portrait(image, crop, size=(168, 216))`; `render_portrait(palette, x, y, scale=2)`.

- [ ] Test fixed dimensions, four layers, stable runs, crop rejection, byte identity, more than 500 committed runs, and bounded coordinates.
- [ ] Run portrait tests RED.
- [ ] Add optional pinned Pillow; implement EXIF transpose, fixed crop, autocontrast, mild unsharp mask, four thresholds, and horizontal runs. Require explicit source/output arguments.
- [ ] Generate from `C:\Users\Divyanshu\Downloads\programmer_natural_under_1mb.jpg` without copying the raster.
- [ ] Rerun GREEN and commit `feat: add deterministic vector portrait`.

### Task 5: Build the V2 hero

**Files:** Replace `content.py`; create `hero.py`; replace `render.py`; modify render tests.

**Interface:** `render_hero(data, theme, build_id=dev)`; preserve `render_profile(...)`.

- [ ] Test threshold behavior at 99/100 contributions, portrait/name/role/Nnomi order, stronger mission class, and in-viewBox easter eggs.
- [ ] Run render tests RED.
- [ ] Implement the asymmetrical field note: portrait left, identity right, quiet context, Nnomi trajectory, thresholded telemetry, bottom rail. Remove fake labels/grid/old positioning/Chauffit from the hero.
- [ ] Rerun GREEN and commit `feat: rebuild profile hero`.

### Task 6: Rebuild the systems narrative

**Files:** New `systems.py`; facade and render tests.

**Interface:** `render_systems_panel(theme, build_id=dev)`; preserve `render_systems(...)`.

- [ ] Test 1200 × 420 geometry, non-equal modules, DAG → aviation → JARVIS order, precise facts, and absence of the `HYBRID AI` headline.
- [ ] Run the focused systems test RED.
- [ ] Draw DAG approvals/incentives/crawler logic, aviation history/forecast with D+65 evidence, and the largest JARVIS phone → policy router → local/cloud module.
- [ ] Rerun GREEN and commit `feat: rebuild systems narrative`.

### Task 7: Rewrite the README

**Files:** `README.md`, repository contract tests.

**Interface:** Consume the four SVGs; produce a GitHub-native supporting narrative.

- [ ] Run the new README contract RED against the old numbered headings, store status, and badge-like ribbons.
- [ ] Write Building, Things I built because I could, Current obsessions, Outside the terminal, and Find me. Give Nnomi two short paragraphs and Chauffit one. Keep telemetry/privacy collapsed.
- [ ] Rerun GREEN and commit `docs: rewrite profile story`.

### Task 8: Make generation and workflows freshness-safe

**Files:** `generate.py`, both workflows, `CONTRIBUTING.md`, generator/repository tests.

**Interface:** Pass one source fingerprint to all render calls; SVG roots carry a 12-hex `data-build` value.

- [ ] Test all four committed assets against the current fingerprint and require workflow coverage for every input while excluding assets from push triggers.
- [ ] Run generator/repository tests RED.
- [ ] Implement fingerprinted atomic generation and paths while preserving schedule, dispatch, least privilege, and four-file bot commits.
- [ ] Regenerate offline, rerun GREEN, and commit `ci: enforce fresh profile assets`.

### Task 9: Perform two visual QA iterations

**Files:** New `docs/design-review/profile-v2-qa.md`; renderer/tests/assets as findings require.

- [ ] Render both SVGs in both themes at 1200 and 880 through width-100% HTML wrappers.
- [ ] Record concrete iteration-1 defects for portrait, typography, Nnomi hierarchy, alignment, light contrast, clipping, and AI-template smell.
- [ ] Tighten a failing contract before each implementation fix.
- [ ] Render iteration 2; repeat until no recognizability, collision, contrast, hierarchy, or generic-template MAJOR remains.
- [ ] Commit `polish: complete profile visual qa`.

### Task 10: Copy sweep, supervisor review, and final verification

**Files:** Public copy, renderer, tests, assets, and QA record as findings require.

- [ ] Run clarity, voice, so-what, proof, specificity, emotional-texture, and friction sweeps; remove buzzword stacks, symmetrical AI copy, filler, and explanations of cleverness.
- [ ] Score five-second, uniqueness, AI-smell, reference, copyability, and identity gates; revise any score below 8/10.
- [ ] Classify findings BLOCKER/MAJOR/MINOR and resolve all BLOCKER/MAJOR items.
- [ ] Run all tests, compileall, generation twice, `git diff --check`, and status.
- [ ] Compare main vs rebuild at 1200 and 880; commit only if the rebuild clearly wins.
- [ ] If main is clean and every gate passes, fast-forward main, rerun tests there, and deliver the required final report.
