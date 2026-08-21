# Profile V2 visual QA

Date: 2026-08-22

Renderer: headless Microsoft Edge, device scale factor 1, width-responsive HTML
wrappers with the SVG displayed at 100% width.

## Inspection matrix

| Asset | Theme | Native | GitHub width |
| --- | --- | ---: | ---: |
| Hero | dark | 1200 x 560 | 880 x 411 |
| Hero | light | 1200 x 560 | 880 x 411 |
| Systems | dark | 1200 x 420 | 880 x 308 |
| Systems | light | 1200 x 420 | 880 x 308 |

Every cell in the matrix was rendered and inspected in both iterations.

## Baseline comparison

The rejected hero used an unrecognizable ASCII approximation, a full-field grid,
repeated numbered terminal labels, a cramped activity line, and equal visual weight
for Nnomi and secondary information. The systems panel gave three equal cards to
unequal stories. The README repeated identity copy and used code-styled ribbons for
headings, skills, and interests.

V2 uses one portrait-led field note, a deliberate identity-to-mission reading path,
Nnomi as the only hero project, four quiet easter eggs, and a separate asymmetric
engineering progression. The rebuild is more legible, more specific to Divyanshu,
and materially stronger than the baseline at both inspected widths.

## Iteration 1 critique

### MAJOR

- The light portrait reversed the source tonal direction and read like a negative.
- The portrait included too much lower torso and desk clutter; the face was
  recognizable but not dominant enough.

### MINOR

- The aviation evidence values had only a narrow visual gap at 1200 px and appeared
  joined at 880 px.
- Supporting metadata becomes intentionally quiet at 880 px. It remains legible and
  does not carry primary meaning, so no size increase was needed.

### Changes

- Reordered the light portrait tones from dark source values to dark output values.
- Tightened the deterministic crop from a desk-heavy composition to head and
  shoulders while retaining the monitor edge and hoodie silhouette.
- Increased the evidence-column separation and protected it with a geometry test.
- Added contracts for portrait tonal direction and crop bounds.

## Iteration 2 critique

- Portrait: glasses, beard, hairline, face shape, and hoodie remain recognizable at
  880 px in both themes.
- Hierarchy: portrait and name land first; role and signature line follow; Nnomi is
  the only project in the hero and is unmistakably the current mission.
- Typography: display copy uses system sans; monospace is limited to context,
  telemetry, engineering annotations, and easter eggs.
- Alignment: no clipped text, baseline collisions, orphan labels, or elements beyond
  either viewBox.
- Light mode: warm paper, graphite ink, restrained amber/teal, and natural portrait
  tones feel authored rather than inverted.
- Systems: DAG to aviation to JARVIS reads left to right; JARVIS is the largest
  module; evidence and diagrams remain distinct at 880 px.
- Template smell: no badge wall, generic stats card, fake shell prompt, or repeated
  numbered labels remains.

No BLOCKER or MAJOR visual finding remains after iteration 2.

## Iteration 3: supervisor copy fixes

The line-by-line requirements audit found two MAJOR copy omissions: the approved
degree had been shortened to an acronym, and the DAG module did not explicitly name
the alternative-consensus experiment. The full degree now fits at 1200 and 880 px
without colliding with the location or work lines. The DAG subtitle and storage note
now state the consensus and linear-chain-growth ideas directly.

The complete eight-render matrix was repeated after those longer lines were added.
No clipping, overlap, or hierarchy regression appeared.

The README was also rendered through GitHub's Markdown API and inspected at 880 px.
Hero-to-heading spacing, Nnomi/Chauffit rhythm, systems placement, heading rules,
outside-the-terminal copy, link rail, and collapsed telemetry disclosure all render
cleanly. A link audit returned 200 for Nnomi and Chauffit. The old X handle returned
404 while a known active X account returned 200, so the stale X link was removed.

## Design-critic gates

| Gate | Score | Reason |
| --- | ---: | --- |
| Five-second | 10/10 | Name, AI/founder identity, and Nnomi are visible without scrolling. |
| Uniqueness | 9/10 | The recognizable portrait, Nnomi journey, edge-AI story, and easter eggs form a specific identity. |
| AI smell | 9/10 | The composition has deliberate asymmetry, edited copy, and useful negative space. |
| Reference | 9/10 | Andrew Grant's current profile remains a memorable single visual; V2 keeps that clarity while replacing the data wall with a founder mission and authored portrait. |
| Copyability | 9/10 | Theme-aware SVGs, deterministic portrait runs, tested geometry, and privacy-safe telemetry make the repository worth inspecting. |
| Identity | 10/10 | Removing the name would still leave a distinctive combination of portrait, Nnomi, JARVIS, system history, and personality. |

Reference inspected: <https://github.com/Andrew6rant/Andrew6rant> at 880 px.

## Visual verdict

PASS. The rebuild clearly beats the preserved baseline and meets the visual bar for
the final supervisor review.

## Final supervisor findings

### BLOCKER

- None.

### MAJOR

- Full approved education line missing from the hero: resolved and regression-tested.
- Alternative-consensus and linear-chain-growth ideas under-specified: resolved and
  regression-tested.
- Public X link returned 404: removed and protected by a repository contract.

### MINOR

- Supporting hero metadata is intentionally quiet at 880 px. It is readable and does
  not carry the five-second message, so no further enlargement was accepted.
- Chauffit currently resolves to a parked public domain rather than a product page.
  The profile keeps the approved product description but makes no release-status
  claim.

All BLOCKER and MAJOR findings are resolved.
