# Profile Copy and Motto Placement Design

**Status:** Approved in conversation

## Objective

Refine the final personal section and philosophical motto without disturbing the approved Profile V2 hierarchy or visual language.

## Approved copy

Replace the separate Porsche and BMW sentence with:

> F1, football, watches, music, coffee, and taking hardware apart with unjustified confidence. German cars remain a recurring threat to the investment plan.

This keeps the voice human and lightly self-aware. Porsche remains discoverable through the existing `garage_target .. 911` easter egg instead of being explained twice.

## Approved placement

Move `build weird things. make them useful. ship them.` out of the `Outside the terminal` section and place it immediately below the systems visual. Render it as a centered, bold, sans-serif paragraph using GitHub-native HTML rather than a Markdown blockquote.

The line becomes an editorial bridge between the engineering evidence and the shorter personal sections. Removing the blockquote also removes GitHub's indented rule and mismatched margins.

## Punctuation contract

Remove em dashes from all public profile content, accessible metadata, and generated assets. Use commas, periods, colons, centered dots, or parentheses according to context. Add a repository contract so em dashes cannot silently return to public output.

## Scope

- README copy and motto placement
- Public hero copy and accessible metadata
- Generated dark and light assets
- Regression tests for punctuation and placement
- Visual review at native width and approximately 880 px

The approved visual system, portrait, Nnomi hierarchy, systems composition, telemetry behavior, and privacy boundary remain unchanged.

## Acceptance criteria

- The new personal copy reads naturally and preserves Divyanshu's personality.
- The motto is visually centered and no longer inherits blockquote styling.
- The motto follows the systems visual and precedes `Current obsessions`.
- No em dash appears in README or generated public SVGs.
- Dark and light assets remain valid, deterministic, distinct, aligned, and legible at 1200 px and approximately 880 px.
- All automated tests pass.
