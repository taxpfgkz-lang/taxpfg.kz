---
phase: 01-baseline-audit-ui-design-contract
plan: 02
subsystem: ui
tags: [css, important-budget, vendor-override, gudfin, swiper, aos, chart.js, audit]

# Dependency graph
requires:
  - phase: 01-baseline-audit-ui-design-contract (01-01)
    provides: baseline research (RESEARCH Q4/Q5, do-not-touch namespaces)
provides:
  - "01-CONFLICT-CATALOG.md: full !important ledger (57 functional decls / 59 grep-c lines) with vendor-rule attribution"
  - "do-not-touch namespace boundary (swiper-*, data-aos*, pbmit-*) with per-namespace breakage analysis"
  - "off-canvas-safe + load-order conflict-surface boundaries cross-referenced"
  - "chart.js disposition: vendored-but-unused, removal deferred to v2/PERF-02"
affects: [phase-02-css-refactor, phase-03, phase-04, phase-05, PERF-02]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "net-new ≈ 0 !important budget floor anchored to a verified ledger (57 functional / 59 grep-c)"
    - "uncited vendor targets explicitly flagged for Phase 2 confirmation"

key-files:
  created:
    - .planning/phases/01-baseline-audit-ui-design-contract/01-CONFLICT-CATALOG.md
  modified: []

key-decisions:
  - "Baseline 59 = grep -c line count (includes 3 comment-prose lines); functional declaration budget = 57 tokens across 56 lines — both reconciled, no silent mismatch"
  - "chart.js removal explicitly OUT OF SCOPE for v1.0 → v2/PERF-02"

patterns-established:
  - "Pattern 1: !important ledger reconciles grep-c (line) vs functional (declaration) counts so Phase 2 has an unambiguous floor"
  - "Pattern 2: uncited vendor targets marked so Phase 2 confirms the beaten selector before relocating an override"

requirements-completed: [AUD-03]

coverage:
  - id: D1
    description: "Full !important ledger from custom.css with file:line + vendor-rule attribution, reconciled to the 59 baseline"
    requirement: "AUD-03"
    verification:
      - kind: automated_ui
        ref: "grep -qiE 'important ledger' 01-CONFLICT-CATALOG.md && grep -q '59'"
        status: pass
    human_judgment: false
  - id: D2
    description: "Do-not-touch namespaces (swiper-*, data-aos*, pbmit-*) + off-canvas/load-order boundaries + chart.js disposition"
    requirement: "AUD-03"
    verification:
      - kind: automated_ui
        ref: "grep do-not-touch/swiper/data-aos/chart.js in 01-CONFLICT-CATALOG.md"
        status: pass
    human_judgment: false

# Metrics
duration: 8min
completed: 2026-06-25
status: complete
---

# Phase 01 Plan 02: Conflict Catalog (AUD-03) Summary

**`01-CONFLICT-CATALOG.md` documenting the full custom.css `!important` ledger (57 functional declarations / 59 grep-c lines, reconciled), the do-not-touch theme namespaces (swiper-*/data-aos*/pbmit-*) with per-namespace breakage analysis, and the chart.js vendored-but-unused disposition deferred to v2/PERF-02.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-06-25T20:36:00Z
- **Completed:** 2026-06-25T20:44:00Z
- **Tasks:** 2
- **Files modified:** 1 (created)

## Accomplishments
- Built the complete `!important` ledger: every functional occurrence in `css/custom.css` tabulated with custom.css line, selector, property, and the vendor rule it beats. 24 declarations cite an exact vendor `file:line`; 31 are flagged **uncited** for Phase 2 to confirm.
- Reconciled the count: `grep -c '!important'` = **59** (matches AUD-03/ROADMAP baseline exactly), of which 3 are comment-prose lines (317, 643, 644) → **57 functional declarations across 56 lines** is the true net-new ≈ 0 budget floor. No silent mismatch — both figures explained.
- Enumerated the do-not-touch namespaces with concrete breakage: `swiper-*` (kills slider + marquee + custom.js `initMarqueeSpeed`), `data-aos*` (AOS reads attrs at init → invisible content), `pbmit-*` (every ledger override targets these; renaming detaches the whole custom layer).
- Cross-referenced the off-canvas-safe constraint (no filter/backdrop-filter/transform on off-canvas ancestors) and the load-order constraint (custom.css/custom.js must load last).
- Documented chart.js as vendored-but-unused (zero HTML references, re-verified live), removal deferred to v2/PERF-02.

## Task Commits

1. **Task 1 + Task 2 (single artifact: 01-CONFLICT-CATALOG.md)** - `4c6e4df` (docs)

Both tasks write to the same single document, so the catalog was committed once as one atomic artifact covering the ledger (Task 1) and the do-not-touch + chart.js sections (Task 2).

**Plan metadata:** _(this commit)_ (docs: complete plan)

## Files Created/Modified
- `.planning/phases/01-baseline-audit-ui-design-contract/01-CONFLICT-CATALOG.md` - The AUD-03 conflict catalog: !important ledger, do-not-touch namespaces, chart.js disposition.

## Decisions Made
- **Baseline reconciliation:** kept "59" valid as the grep-c line count (= AUD-03 baseline) while surfacing the functional declaration budget of 57 — Phase 2 diffing real rules should target 57, grep-based audits stay at 59.
- **Uncited targets flagged, not guessed:** rather than invent vendor selector/line for the 31 overrides whose comments don't cite a beaten rule, they are marked "uncited" so Phase 2 confirms before touching. Avoids fabricated attribution.
- **chart.js deferred:** removal kept out of v1.0 scope to prevent a later phase "discovering" and acting on it mid-milestone.

## Deviations from Plan

None - plan executed exactly as written. The two tasks both target one document, so a single atomic commit covers both (verification greps for Task 1 and Task 2 both pass against the committed file).

## Issues Encountered
None. Static analysis only; `git status` confirmed no new edits to `css/*`, `js/*`, or `*.html`. (CRLF warning on commit is cosmetic — Git autocrlf on Windows.)

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 2 (CSS refactor) has its override floor (57 functional / 59 grep-c) and the hard do-not-touch boundary.
- 31 uncited vendor targets are the first thing Phase 2 should confirm before relocating any override.
- chart.js disposition recorded; no action this milestone.

## Self-Check: PASSED
- FOUND: .planning/phases/01-baseline-audit-ui-design-contract/01-CONFLICT-CATALOG.md
- FOUND: commit 4c6e4df

---
*Phase: 01-baseline-audit-ui-design-contract*
*Completed: 2026-06-25*
