---
phase: 02-design-tokens-primitives
plan: 01
subsystem: ui
tags: [css, design-tokens, custom-properties, spacing-scale, fluid-typography, clamp, z-index]

# Dependency graph
requires:
  - phase: 01-baseline-audit-ui-design-contract
    provides: 01-UI-SPEC contract (spacing/type values), AUD-03 !important budget floor (grep-c=59)
provides:
  - "--pfg-space-* 4px spacing scale (1/2/3/4/6/8/12/16/24 → 4..96px)"
  - "--pfg-fs-* fluid clamp() type scale (body/label/h2-h6/display, ratio ~1.25) + --pfg-lh-tight/-body/-display"
  - "--pfg-z-float z-index token consolidating the single hardcoded z-index:9999"
affects: [02-02, 03-components, 04-conversion-blocks]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Additive :root extension — new token groups appended, existing --pfg-* tokens byte-identical (rename breaks every var() consumer)"
    - "clamp() MAX mirrors vendor desktop-px so 1440 desktop renders non-regressively; MIN supplies mobile fluidity"
    - "Single-consumer z-index token (no speculative scale) per 02-RESEARCH Open Question 2"

key-files:
  created:
    - .planning/phases/02-design-tokens-primitives/02-01-SUMMARY.md
  modified:
    - css/custom.css

key-decisions:
  - "Token sheet extended additively — no existing --pfg-* token renamed/reordered (var() refs intact)"
  - "Heading clamp() maxes locked to vendor px (h1 58 / h2 48 / h3 40 / h4 34 / h5 28 / h6 22) so desktop stays byte-identical; application deferred to 02-02"
  - "z-index token declared for the one real consumer (whatsapp-float) only; no multi-level scale invented"
  - "Declaration-only plan — no selectors restyled, tokens not yet applied to elements (that is 02-02)"

patterns-established:
  - "Pattern: 4px spacing grid named by multiplier (--pfg-space-4 = 4*4 = 16px)"
  - "Pattern: fluid type via clamp() with desktop-max = vendor px for non-regression during declaration phase"

requirements-completed: [TOK-01, TOK-02, TOK-03]

coverage:
  - id: D1
    description: "--pfg-space-* 4px spacing scale declared in :root (9 tokens, 4..96px)"
    requirement: "TOK-02"
    verification:
      - kind: other
        ref: "grep -c -- '--pfg-space-' css/custom.css == 9; --pfg-space-4:16px, --pfg-space-6:24px"
        status: pass
    human_judgment: false
  - id: D2
    description: "--pfg-fs-* fluid clamp() type scale + --pfg-lh-* line-heights declared; clamp maxes mirror vendor desktop px"
    requirement: "TOK-03"
    verification:
      - kind: other
        ref: "grep -c -- '--pfg-fs-' css/custom.css == 8; h2 max 3rem=48px, display max 3.625rem=58px match base.css:223-251"
        status: pass
    human_judgment: false
  - id: D3
    description: "--pfg-z-float token consolidates the single hardcoded z-index:9999 (whatsapp-float now references it)"
    requirement: "TOK-01"
    verification:
      - kind: other
        ref: "grep -n 'var(--pfg-z-float)' css/custom.css matches .pfg-whatsapp-float; --pfg-z-float:9999 declared"
        status: pass
    human_judgment: false
  - id: D4
    description: "Additive-only edit — existing --pfg-* tokens untouched, !important budget unchanged"
    verification:
      - kind: other
        ref: "grep -c '!important' css/custom.css == 59; git diff shows 0 removed --pfg-* declarations (only z-index:9999 swap)"
        status: pass
    human_judgment: false

# Metrics
duration: 6min
completed: 2026-06-25
status: complete
---

# Phase 2 Plan 01: Design Token Foundation Summary

**Extended the custom.css :root with a 4px spacing scale, a fluid clamp() type scale (ratio ~1.25), and a single z-index token — additively, with desktop rendering held byte-identical.**

## Performance

- **Duration:** ~6 min
- **Started:** 2026-06-25T21:45:00Z
- **Completed:** 2026-06-25T21:51:00Z
- **Tasks:** 1
- **Files modified:** 1 (css/custom.css)

## Accomplishments
- Declared `--pfg-space-1..24` (4/8/12/16/24/32/48/64/96px) — the 4px grid for TOK-02
- Declared fluid `--pfg-fs-body/-label/-h6/-h5/-h4/-h3/-h2/-display` clamp() scale plus `--pfg-lh-tight/-body/-display` for TOK-03; each heading clamp MAX mirrors the vendor desktop px (58/48/40/34/28/22) so the 1440 desktop is non-regressive
- Consolidated the lone hardcoded `z-index:9999` (whatsapp-float) into `--pfg-z-float` and switched the rule to `var(--pfg-z-float)` — completing the TOK-01 consolidation
- Held the additive contract: every existing `--pfg-ink … --pfg-tf` token is byte-identical and the `!important` budget stays at 59

## Task Commits

1. **Task 1: Extend :root with spacing + type + z-index tokens (additive)** - `af45231` (feat)

**Plan metadata:** committed separately with SUMMARY/STATE/ROADMAP

## Files Created/Modified
- `css/custom.css` - :root token sheet extended with three additive groups (spacing, fluid type, z-index); whatsapp-float z-index now references `--pfg-z-float`

## Decisions Made
- Additive-only extension: existing `--pfg-*` tokens left untouched to avoid silently breaking any `var()` consumer (02-RESEARCH caveat).
- Heading clamp() maxes locked to vendor px so this declaration phase produces zero desktop visual change; element application is deferred to 02-02.
- No multi-level z-index scale — only the single real consumer exists (02-RESEARCH Open Question 2).

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None. (Note: `grep -c ':root{'` reports 2 — the pre-existing vendor-color override at custom.css:122 plus the token sheet at :284. No second token block was introduced.)

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Token foundation (spacing + fluid type + z-index) is declared and ready for application in plan 02-02 (snap element padding/margins to `--pfg-space-*`, wire headings/body to `--pfg-fs-*`, input font-size 16px).
- No blockers. Desktop render unchanged; mobile fluidity activates only once tokens are applied in 02-02.

---
*Phase: 02-design-tokens-primitives*
*Completed: 2026-06-25*

## Self-Check: PASSED
- css/custom.css modified, committed in af45231
- 02-01-SUMMARY.md present
