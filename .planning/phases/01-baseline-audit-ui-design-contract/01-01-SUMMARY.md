---
phase: 01-baseline-audit-ui-design-contract
plan: 01
subsystem: testing
tags: [lighthouse, axe-core, playwright, a11y, wcag, baseline, audit]

# Dependency graph
requires: []
provides:
  - "Committed per-page Lighthouse baseline (a11y/perf/CLS/LCP) for all 11 pages under baseline/lighthouse/"
  - "Committed per-page axe-core WCAG 2.0/2.1 A+AA violations baseline (0 violations) under baseline/axe/"
  - "01-AUDIT.md AUD-01 regression-floor table (min a11y=95, axe=0) + AUD-02 placeholder for plan 01-03"
affects: [01-03-visual-audit, 01-04-design-contract, phase-05-a11y-verification, AUD-01, A11Y-04, VER-01]

# Tech tracking
tech-stack:
  added: []  # all audit tooling npx-ephemeral / out-of-repo; nothing persisted into the no-build site
  patterns:
    - "Audit tooling runs ephemerally (npx + out-of-tree C:/gsdtmp runner) — no package.json/lockfile added to the no-build site"
    - "All audits served over http://127.0.0.1:8080 (python http.server), never file://, so relative assets + @import fonts + Maps iframe resolve"
    - "baseline/ artifacts live under .planning/ (not repo root) so they are NOT gitignored and persist as the committed regression floor"

key-files:
  created:
    - ".planning/phases/01-baseline-audit-ui-design-contract/01-AUDIT.md"
    - ".planning/phases/01-baseline-audit-ui-design-contract/baseline/lighthouse/ (11 JSON + 11 HTML)"
    - ".planning/phases/01-baseline-audit-ui-design-contract/baseline/axe/ (11 JSON)"
  modified: []

key-decisions:
  - "Pinned lighthouse@13.4.0 and @axe-core/playwright@4.12.1 for reproducibility (RESEARCH State-of-the-Art)"
  - "Bound server to 127.0.0.1 (not localhost) and audited 127.0.0.1 URLs to avoid Windows localhost->IPv6 mismatch"
  - "Ran axe via an out-of-repo C:/gsdtmp/axe-runner (ASCII path) instead of @axe-core/cli to dodge chromedriver flakiness and the Cyrillic-path EPERM bug; nothing installed into the site tree"
  - "Scanned axe tags wcag2a/2aa/21a/21aa only; the known mobile-header target-size flag is WCAG 2.2 SC 2.5.8 (outside scanned tags) so it is recorded as an accepted exception, not a violation"

patterns-established:
  - "Regression-floor capture: Lighthouse JSON+HTML + axe JSON per page, summarized in an AUD-01 table with an explicit min-a11y floor note"

requirements-completed: [AUD-01]

coverage:
  - id: D1
    description: "Per-page Lighthouse baseline (a11y/perf/CLS/LCP) captured for all 11 pages over http://127.0.0.1:8080"
    requirement: "AUD-01"
    verification:
      - kind: automated_ui
        ref: "ls baseline/lighthouse/*.report.json == 11; each JSON has non-null accessibility+performance scores and CLS+LCP numericValues"
        status: pass
    human_judgment: false
  - id: D2
    description: "Per-page axe-core WCAG 2.0/2.1 A+AA violations baseline (0 violations) captured for all 11 pages"
    requirement: "AUD-01"
    verification:
      - kind: automated_ui
        ref: "ls baseline/axe/*.json == 11; each contains a violations array (all empty)"
        status: pass
    human_judgment: false
  - id: D3
    description: "01-AUDIT.md AUD-01 11-row regression-floor table + floor note (min a11y=95) + AUD-02 placeholder"
    requirement: "AUD-01"
    verification:
      - kind: automated_ui
        ref: "grep AUD-01 && 11 page rows matched; grep AUD-02 placeholder present"
        status: pass
    human_judgment: false

# Metrics
duration: 8min
completed: 2026-06-25
status: complete
---

# Phase 01 Plan 01: Baseline Audit Capture Summary

**Committed AUD-01 regression floor — Lighthouse (a11y 95-96, perf 55-57, CLS/LCP) + axe-core WCAG 2.0/2.1 A+AA (0 violations) across all 11 pages, served over local HTTP, with zero site-code changes.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-06-25T20:29:50Z
- **Completed:** 2026-06-25T20:37:53Z
- **Tasks:** 3
- **Files modified:** 23 created (11 LH JSON + 11 LH HTML + 11 axe JSON + 01-AUDIT.md), 0 site files

## Accomplishments
- Captured Lighthouse performance + accessibility reports (JSON + HTML) for all 11 pages over `http://127.0.0.1:8080`, pinned to lighthouse@13.4.0
- Captured axe-core WCAG 2.0/2.1 A+AA violation reports for all 11 pages via @axe-core/playwright 4.12.1 — **0 violations everywhere**
- Wrote `01-AUDIT.md` with the AUD-01 11-row regression-floor table (a11y/perf/CLS/LCP/axe-count), an explicit floor note (min a11y = 95), the WCAG 2.2 target-size accepted-exception note, and the AUD-02 placeholder for plan 01-03
- No site code touched — `css/*`, `js/*`, `*.html` left byte-identical (pre-existing working-tree edits untouched)

## Task Commits

1. **Task 1: Lighthouse across all 11 pages** - `ff10a3b` (chore)
2. **Task 2: axe-core WCAG scan across all 11 pages** - `a814730` (chore)
3. **Task 3: AUD-01 per-page baseline table** - `bc4a6d7` (docs)

## Files Created/Modified
- `.planning/phases/01-baseline-audit-ui-design-contract/baseline/lighthouse/<slug>.report.{json,html}` - raw Lighthouse floor, 11 pages
- `.planning/phases/01-baseline-audit-ui-design-contract/baseline/axe/<slug>.json` - raw axe violations floor, 11 pages
- `.planning/phases/01-baseline-audit-ui-design-contract/01-AUDIT.md` - AUD-01 baseline table + floor note + AUD-02 placeholder

## Baseline values (the committed floor)

| Metric | Floor |
|---|---|
| Min accessibility score (across 11 pages) | **95** (index/services/contacts = 96) |
| axe-core WCAG 2.0/2.1 A+AA violations | **0** on all 11 pages |
| Performance | 55-57 (reference only, not a gate this milestone) |
| CLS | 0.000 all pages except index.html (0.077, still "good") |
| LCP | ~9-10 s inner pages; index.html outlier ~15.4 s (hero slider) |

## Decisions Made
- **Pinned tool versions** (lighthouse@13.4.0, @axe-core/playwright@4.12.1) for reproducibility.
- **127.0.0.1 instead of localhost** — avoids Windows localhost→IPv6 (::1) binding mismatch with `python -m http.server`.
- **Out-of-repo axe runner** at `C:/gsdtmp/axe-runner` (ASCII path) using Playwright + @axe-core/playwright rather than `@axe-core/cli` — sidesteps chromedriver flakiness and the Cyrillic-path EPERM teardown bug. Nothing was installed into the site tree (no-build constraint preserved).
- **axe tag scope** = wcag2a/2aa/21a/21aa. The accepted mobile-header target-size exception is WCAG 2.2 SC 2.5.8, outside this scope, so it does not appear in (and does not inflate) the 0-violation floor; it is documented as a standing exception for plan 01-03.

## Deviations from Plan

None - plan executed exactly as written. Task 2 allowed the @axe-core/playwright path explicitly; choosing it over the CLI fallback is within the plan's stated options.

## Issues Encountered
- **Lighthouse non-fatal EPERM at temp cleanup:** On this Windows + Cyrillic-username host, lighthouse prints `EPERM ... rmSync ... \\?\C:\Users\836D~1\AppData\Local\Temp\lighthouse.*` from chrome-launcher `destroyTmp` **after** the report is already written. Verified all 11 JSON/HTML reports are complete and contain valid scores; the error is cosmetic temp-dir teardown only. Documented in 01-AUDIT.md reproduce notes.
- **axe "Please use browser.newContext()":** @axe-core/playwright 4.12.1 rejects pages opened directly off `browser.newPage()`; fixed by opening pages from an explicit `browser.newContext()`. Resolved before any artifact was committed.

## User Setup Required
None - no external service configuration required. Audit tooling is ephemeral/out-of-tree.

## Next Phase Readiness
- AUD-01 dependency gate is satisfied and committed — plans 01-02, 01-03, 01-04 can proceed.
- Plan 01-03 should append its block under the existing `## AUD-02 — Visual problems by block-type` placeholder and log the WCAG 2.2 target-size flag as an accepted exception.
- Phase 5 (A11Y-04, VER-01) now has a concrete floor to measure against: keep every page's a11y score >= its baseline row (hard floor 95) and axe violations at 0 for the scanned tag set.

---
*Phase: 01-baseline-audit-ui-design-contract*
*Completed: 2026-06-25*

## Self-Check: PASSED
- 01-AUDIT.md, 01-01-SUMMARY.md exist
- 11 Lighthouse JSON + 11 axe JSON present
- Task commits ff10a3b, a814730, bc4a6d7 verified in git log
