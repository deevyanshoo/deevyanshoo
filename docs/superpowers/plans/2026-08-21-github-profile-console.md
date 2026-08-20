# GitHub Profile Console Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a distinctive, accessible, privacy-safe, automatically refreshed GitHub profile for `deevyanshoo`.

**Architecture:** Map a scalar-only GraphQL response into frozen aggregate data and pass it to a pure SVG renderer. Keep secrets away from pull requests and native Markdown below the artwork.

**Tech Stack:** Python 3.13 standard library, `unittest`, SVG, GitHub GraphQL API, GitHub Actions v7.

## Global Constraints

- Never request, persist, log, or render private repository identifiers.
- Use only `runtime v26`; no DOB/time.
- Avoid badges, followers, streaks, and language percentages.
- Render the same input to byte-identical output.

### Task 1: Privacy and rendering contract

- [ ] Write failing tests for query safety, data minimization, escaping, themes, deterministic SVG, and leakage.
- [ ] Run tests and verify the failure is the missing package.

### Task 2: Typed telemetry and renderer

- [ ] Implement frozen aggregate models and scalar-only GraphQL parsing/fetching.
- [ ] Add approved portrait/content constants and pure SVG composition.
- [ ] Run tests to green.

### Task 3: Generator, README, and workflows

- [ ] Add failing contract tests for offline generation, README accessibility, and workflow policy.
- [ ] Implement the CLI, fallback fixture, README, maintenance docs, and least-privilege workflows.
- [ ] Generate committed light/dark assets twice and require byte stability.

### Task 4: Verification and publication

- [ ] Run tests, compile checks, privacy scans, deterministic builds, and visual inspection.
- [ ] Request independent review and fix critical/important findings.
- [ ] Restore Git metadata, commit confirmed paths, publish to `main`, and verify remote state.
