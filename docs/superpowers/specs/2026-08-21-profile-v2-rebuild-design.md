# GitHub Profile V2 Rebuild Design

**Status:** Approved by the supplied autonomous-execution brief

**Objective:** Build a GitHub profile that reads in five seconds as “Divyanshu Goyal builds ambitious AI systems and companies,” then rewards closer inspection with specific engineering evidence and personality.

## Audit of the rejected profile

The existing implementation is technically sound but visually generic. The hero behaves like a boxed dashboard, labels such as `IDENTITY // 00` and `PORTRAIT // ASCII SCAN` narrate the interface instead of letting it communicate, and the portrait is not recognizable. Nnomi is a small text block rather than the current mission. The three systems are three equal résumé cards, the README repeats identity copy directly below the hero, and pills/code formatting flatten every subject into the same visual weight.

At native width, the existing hero is legible but crowded. Its top-right telemetry is cramped, its footer is overfilled, and the light theme looks like a mechanical inversion. At a narrow viewport the SVG is clipped when it is not explicitly scaled. These are regression cases for the rebuild.

## Considered directions

### 1. Terminal dashboard

Keep the current panel grammar but improve spacing, portrait fidelity, and typography. This is the lowest-risk engineering option, but it preserves the rejected “fake terminal” idea and makes the profile feel assembled from familiar AI-profile parts.

### 2. Operator field note — selected

Use an asymmetrical editorial composition: a recognizable monochrome portrait on the left dissolves into scanlines and a restrained signal path; the right carries a large human identity block; Nnomi occupies the lower visual field as a wealth journey rather than a card. Bloomberg influence appears in alignment, microcopy, and tabular data—not in a wall of metrics. AI-lab influence appears in the portrait treatment and signal routing. GitHub restraint comes from negative space, system typography, and minimal decoration.

This direction best unifies engineer, AI builder, and founder without turning the hero into a résumé.

### 3. Research blueprint poster

Make the hero a technical schematic with identity as an annotation. It would be distinctive, but it weakens the five-second identity test and makes the portrait and founder story secondary.

## Visual concept

The hero is a 1200 × 560 SVG designed to be embedded at `width=100%` and inspected at 1200 px and 880 px. The composition is intentionally asymmetric:

- The left 37% is a head-and-shoulders portrait derived deterministically from the selected desk photograph. Four grayscale/duotone vector layers preserve the glasses, beard, hairline, jaw, and hoodie. Sparse scanlines and a soft edge dissolve connect the image to the interface without labeling the treatment.
- The upper-right field contains the name at the strongest typographic scale, followed by `AI Architect · Founder · Builder` and the signature line `making large models fit small boxes`.
- The lower-right field is Nnomi. Its name, concise product framing, and `earn → see clearly → protect → invest → build wealth` path are the second visual anchor. It is not enclosed in a generic card.
- ZS, Penn, and `Gurugram ↔ wherever` form one quiet context line. ZS remains secondary.
- A single aggregate GitHub contribution signal may appear only when it clears its threshold. It never competes with identity or Nnomi.
- The four approved easter eggs occupy a low-contrast bottom rail. No additional joke is needed.

The dark palette uses graphite black, off-white, warm amber, and a small amount of muted cyan. The light palette uses warm ivory, ink graphite, burnt amber, and restrained teal; it is tuned independently rather than inverted.

Major identity text uses the GitHub/system sans stack. Monospace is limited to telemetry, technical annotations, and easter eggs. Borders are used as alignment rules, not as containers around every concept.

## Portrait pipeline

The recovered local desk/hoodie photograph is an input, not a public asset. An optional Pillow-based script accepts an explicit local source path, applies a fixed crop, corrects orientation, converts to grayscale, adjusts contrast, quantizes into four tonal bands, and emits deterministic run-length vector data. The generated vector data is committed; the original photograph is not.

The renderer clips the vector layers to an authored silhouette area and adds only deterministic SVG effects. No generative face alteration is used. If the crop fails the recognizability check at 880 px, the crop and thresholds are revised and the vector data regenerated.

## README architecture

1. Theme-aware hero with descriptive alt text. No identity sentence immediately underneath.
2. `Building` with Nnomi first and visibly more copy/space than Chauffit. Nnomi is described as an India-first financial coach moving from earning money to building wealth. Chauffit is described as an AI-powered, safety-first on-demand driver marketplace. Store-release claims are omitted because the current public website is parked and public store searches do not verify them.
3. Theme-aware systems visual under `Things I built because I could`.
4. `Current obsessions` as one restrained sentence, not a badge ribbon.
5. `Outside the terminal` as a short human paragraph.
6. The philosophical line, simple links, and a collapsed telemetry/privacy note.

## Systems visual

The systems SVG is 1200 × 420 and tells a left-to-right progression: distributed systems → large-scale ML → edge AI.

- DAG Ledger begins the story with a compact directed acyclic graph and precise experimental language: peer approvals, crawler/network logic, incentives, and custom consensus exploration.
- Aviation Forecasting anchors the middle with a forecast plot and the approved public-safe evidence: 65 days ahead, greater than 90% accuracy, and approximately 800 TB/day.
- JARVIS is the largest final section. A phone routes inference by privacy, latency, and capability to a quantized local SLM or cloud LLM. This section says what the system is rather than reducing it to “hybrid AI.”

The modules use shared baselines and whitespace instead of three identical bordered cards. At 880 px the SVG scales as one object; all critical labels remain at an effective size of at least roughly 10 px.

## Content model and rendering boundaries

`content.py` owns public prose and structured project/system content. `model.py` owns typed anonymous telemetry. `portrait_data.py` owns generated non-identifying vector runs. Focused renderer modules own SVG primitives, the hero, and the systems composition. `scripts/generate.py` remains the single asset entry point.

SVG output is deterministic for identical content and stats. All dynamic text is escaped. Themes share geometry but have independently authored palettes. Every SVG includes a source fingerprint derived from renderer/content inputs so tests can detect stale committed assets even when live telemetry differs from the offline fixture.

## Telemetry and privacy boundary

The only live visible metric is year-to-date contribution count, and it is hidden below 100. No stars, followers, streaks, repository count, language percentage, or separate private-contribution count is rendered.

The GraphQL query requests only contribution aggregates. It does not request repository nodes or any repository, organization, branch, issue, commit, file, topic, URL, or description field. Unexpected keys are discarded immediately while parsing into the frozen typed model. Private activity can influence only GitHub’s anonymous aggregate total. The renderer receives integers only.

`PROFILE_TOKEN` is optional. With it, a classic token limited to `read:user` can include the account’s allowed aggregate private contribution visibility. Without it, the workflow uses the repository `GITHUB_TOKEN` and still generates a public-safe profile, potentially with a lower aggregate.

## Workflow behavior

CI runs on pushes and pull requests with `contents: read`. It runs unit tests, compilation, deterministic double generation, XML parsing, and stale-asset fingerprint checks.

The refresh workflow runs on schedule, manual dispatch, and changes to content, renderer, portrait data, telemetry, generation logic, or the fixture. It uses `contents: write`, tests before generation, writes only the four generated SVGs, and commits only when bytes change. Asset-only bot commits do not retrigger the workflow because the push path filter excludes `assets/**`, preventing loops.

The repository keeps current stable major versions of `actions/checkout` and `actions/setup-python` (`v7` at the time of this design).

## Error handling

- Invalid themes and invalid/non-integer/negative aggregates fail immediately.
- GraphQL errors, missing aggregate fields, malformed payloads, and network failures fail closed; no partial private data is logged or rendered.
- Live generation without either token exits with an actionable message; offline generation remains available.
- Portrait generation rejects unreadable files, invalid crops, and non-deterministic output dimensions.
- Asset generation writes through temporary files and atomic replacement.

## Test contracts

Tests protect valid XML, deterministic output, distinct light/dark palettes, required identity, Nnomi prominence, all four easter eggs, the Unicode location arrow, escaping, forbidden public implementation language, absence of weak vanity metrics, README asset references, privacy-query allowlisting, workflow permissions/triggers, and source-fingerprint freshness.

Visual QA is a separate acceptance layer. Each meaningful design iteration renders dark and light at 1200 px and 880 px. Review notes classify defects and record fixes. Automated tests cannot waive the five-second, uniqueness, AI-smell, reference, copyability, or identity gates.

## Acceptance

The branch may merge only after multiple visual iterations, a clean copy sweep, passing automated tests, no BLOCKER or MAJOR supervisor findings, and a side-by-side comparison that clearly favors the rebuild. The main worktree remains untouched until then.
