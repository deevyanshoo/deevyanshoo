# Profile Copy and Motto Placement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the awkward car copy, move and restyle the philosophical motto, and remove em dashes from every public profile surface.

**Architecture:** Keep the existing README and deterministic SVG renderer boundaries. Protect copy, placement, and punctuation with repository and renderer contracts, then regenerate the four committed assets through the existing generation entry point.

**Tech Stack:** Python 3.12+, `unittest`, deterministic SVG generation, GitHub-flavored Markdown, headless Chrome

## Global Constraints

- Preserve the portrait, Nnomi journey, systems composition, telemetry threshold, and privacy boundary.
- Motto: `build weird things. make them useful. ship them.`
- Personal copy: `F1, football, watches, music, coffee, and taking hardware apart with unjustified confidence. German cars remain a recurring threat to the investment plan.`
- The motto follows the systems visual and precedes `Current obsessions`.
- README and generated SVGs contain no Unicode em dash.
- Inspect both themes at 1200 px and approximately 880 px.

---

## File map

- `README.md`: public copy, order, alternative text, and motto markup.
- `src/operator_profile/content.py`: public hero education line.
- `tests/test_repository_contract.py`: README placement, copy, and punctuation contracts.
- `tests/test_render.py`: rendered hero punctuation contract.
- `assets/*.svg`: deterministic regenerated assets.
- `docs/design-review/profile-v2-qa.md`: refinement QA record.

### Task 1: Lock README copy and placement

**Files:** Modify `tests/test_repository_contract.py` and `README.md`.

**Interfaces:** Consume GitHub-flavored Markdown. Produce a centered bold motto and exact personal copy.

- [x] **Step 1: Write the failing contract**

```python
def test_personality_copy_and_motto_placement_are_authored(self) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    motto = "build weird things. make them useful. ship them."
    personal = (
        "F1, football, watches, music, coffee, and taking hardware apart "
        "with unjustified confidence. German cars remain a recurring threat "
        "to the investment plan."
    )
    motto_markup = f'<p align="center"><strong>{motto}</strong></p>'
    self.assertIn(personal, readme)
    self.assertIn(motto_markup, readme)
    self.assertNotIn("> **build weird things", readme)
    self.assertNotIn("Porsche has the garage target", readme)
    self.assertLess(readme.index("assets/systems-light.svg"), readme.index(motto))
    self.assertLess(readme.index(motto), readme.index("## Current obsessions"))
```

- [x] **Step 2: Run RED**

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_repository_contract.ReadmeContractTests.test_personality_copy_and_motto_placement_are_authored -v
```

Expected: FAIL because the old copy and blockquote remain.

- [x] **Step 3: Implement**

Move the exact motto below the systems picture and wrap it in `<p align="center"><strong>...</strong></p>`. Replace the personal paragraphs with the exact Global Constraints copy and delete the blockquote.

- [x] **Step 4: Run GREEN**

Repeat Step 2. Expected: one passing test.

### Task 2: Remove public em dashes

**Files:** Modify `tests/test_repository_contract.py`, `tests/test_render.py`, `README.md`, and `src/operator_profile/content.py`. Regenerate `assets/*.svg`.

**Interfaces:** Consume `EDUCATION: str` and `render_profile(ProfileData, Theme) -> str`. Produce public Markdown and SVG strings without `U+2014`.

- [x] **Step 1: Write failing punctuation contracts**

Add to `test_public_assets_exclude_internal_notes_and_vanity_metrics`:

```python
for content in public:
    self.assertNotIn("\u2014", content)
```

Add to `test_profile_has_identity_hierarchy_and_personality`:

```python
self.assertNotIn("\u2014", svg)
```

- [x] **Step 2: Run RED**

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_repository_contract.ReadmeContractTests.test_public_assets_exclude_internal_notes_and_vanity_metrics tests.test_render.DeterministicRenderTests.test_profile_has_identity_hierarchy_and_personality -v
```

Expected: FAIL on the README alternative text and hero education line.

- [x] **Step 3: Replace public em dashes**

Change the README alternative text to:

```html
<img alt="Divyanshu Goyal, AI Architect, founder, and builder; University of Pennsylvania; Gurugram ↔ wherever" src="assets/profile-light.svg" width="100%">
```

Change `EDUCATION` to:

```python
EDUCATION = (
    "MASTER OF SCIENCE IN ENGINEERING · DATA SCIENCE "
    "· UNIVERSITY OF PENNSYLVANIA"
)
```

- [x] **Step 4: Regenerate all assets**

```powershell
$env:PYTHONPATH='src'
python scripts/generate.py --offline
```

Expected: all four SVGs update because the source fingerprint changes.

- [x] **Step 5: Run GREEN and scan**

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_repository_contract tests.test_render -v
rg -n "—|&mdash;|&#8212;" README.md assets
```

Expected: tests pass and `rg` returns no matches.

### Task 3: Regenerate, inspect, and publish

**Files:** Modify `docs/design-review/profile-v2-qa.md`; verify all tracked files.

**Interfaces:** Consume generated assets and GitHub's README renderer. Produce a reviewed commit and matching `profile-v2-rebuild` preview.

- [x] **Step 1: Verify determinism and all tests**

```powershell
$env:PYTHONPATH='src'
python scripts/generate.py --offline
python -m unittest discover -s tests -v
git diff --check
```

Expected: `profile assets unchanged`, all tests pass, and no diff errors.

- [x] **Step 2: Render all eight inspection images**

```powershell
$profileQaDir = Join-Path $env:TEMP 'deevyanshoo-profile-copy-qa'
New-Item -ItemType Directory -Force -Path $profileQaDir | Out-Null
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\profile-dark-1200.png" --window-size=1200,560 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/profile-dark.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\profile-dark-880.png" --window-size=880,411 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/profile-dark.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\profile-light-1200.png" --window-size=1200,560 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/profile-light.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\profile-light-880.png" --window-size=880,411 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/profile-light.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\systems-dark-1200.png" --window-size=1200,420 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/systems-dark.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\systems-dark-880.png" --window-size=880,308 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/systems-dark.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\systems-light-1200.png" --window-size=1200,420 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/systems-light.svg"
& $chrome --headless=new --disable-gpu --hide-scrollbars --screenshot="$profileQaDir\systems-light-880.png" --window-size=880,308 "file:///C:/Users/Divyanshu/deevyanshoo-profile-v2/assets/systems-light.svg"
```

Inspect all PNGs for clipping, alignment, contrast, portrait recognizability, Nnomi hierarchy, and regressions.

Windows note discovered during execution: direct navigation is valid at native
size, but the 880 px pass must use a temporary single-root SVG whose `<image>`
references the source asset at the scaled dimensions. Launch every capture with a
unique `--user-data-dir` and wait for Chrome to exit; shared profiles can race and
produce stale screenshots. The temporary wrappers are QA artifacts and are not
committed.

- [x] **Step 3: Record visual QA**

Append a dated section to `docs/design-review/profile-v2-qa.md` recording the exact copy and motto placement, both themes at 1200 px and 880 px, the absence of clipping or hierarchy regressions, the public em-dash scan, and the verdict.

- [ ] **Step 4: Commit implementation**

```powershell
git add -- README.md src/operator_profile/content.py tests/test_repository_contract.py tests/test_render.py assets/profile-dark.svg assets/profile-light.svg assets/systems-dark.svg assets/systems-light.svg docs/design-review/profile-v2-qa.md docs/superpowers/plans/2026-08-22-profile-copy-placement.md
git commit -m "polish: refine profile personality and motto"
```

Expected: one focused implementation commit.

- [ ] **Step 5: Publish and verify GitHub rendering**

```powershell
git push origin profile-v2-rebuild
gh api -H 'Accept: application/vnd.github.html+json' 'repos/deevyanshoo/deevyanshoo/readme?ref=profile-v2-rebuild'
```

Verify the HTML contains the centered motto before `Current obsessions`, contains the new German-cars sentence, and contains no em dash. Confirm the remote branch SHA matches local `HEAD`.
