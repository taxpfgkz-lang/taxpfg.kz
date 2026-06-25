---
phase: 01-baseline-audit-ui-design-contract
plan: 03
subsystem: ui
tags: [audit, playwright, dom-measurement, wcag, responsive, accessibility, screenshots]

# Dependency graph
requires:
  - phase: 01-01
    provides: AUD-01 baseline (0 axe violations, a11y floor 95), AUD-02 placeholder heading, baseline/axe + baseline/lighthouse
provides:
  - "AUD-02 visual-problem inventory grouped by block-type (what/where/viewport/why/screenshot)"
  - "DOM-measured evidence: baseline/measurements.json (103 boxes) at 1440/1024/768/390/360"
  - "34 block-type screenshots under baseline/screenshots/"
  - "Reproducible Playwright measurement harness (measure.cjs, measure2.cjs)"
  - "Absent-feature ledger (pricing/FAQ/modal) flagged net-new-or-descope"
affects: [01-04, design-contract-reconciliation, phase-2-tokens, phase-4-imagery, phase-5-a11y]

# Tech tracking
tech-stack:
  added: [playwright@1.60.0 (global, gsd-pi vendored — ephemeral, no repo install)]
  patterns:
    - "DOM-measured truth over CSS source text (RESEARCH Pattern 2)"
    - "Block-type grouping over per-page enumeration (RESEARCH Pattern 1)"
    - "Ephemeral external tooling against python http.server :8080 (no-build honored)"

key-files:
  created:
    - .planning/phases/01-baseline-audit-ui-design-contract/baseline/measure.cjs
    - .planning/phases/01-baseline-audit-ui-design-contract/baseline/measure2.cjs
    - .planning/phases/01-baseline-audit-ui-design-contract/baseline/measurements.json
    - .planning/phases/01-baseline-audit-ui-design-contract/baseline/screenshots/ (34 PNG)
  modified:
    - .planning/phases/01-baseline-audit-ui-design-contract/01-AUDIT.md

key-decisions:
  - "Trusted DOM-measured boxes over rendered-pixel inspection (project convention); screenshots committed as evidence"
  - "Force-added baseline/screenshots/ past the generic screenshots/ .gitignore — plan lists it as a required committed artifact (T-01-03); generic ignore left intact for ad-hoc shots"
  - "axe baseline = 0 violations, so every AUD-02 finding rests on a DOM measurement (no axe IDs to fold)"

patterns-established:
  - "Pattern 1: one finding table per block-type, shared chrome audited once with page deltas"
  - "Pattern 2: every Why cites a measured px value or an axe rule, never 'looks off'"

requirements-completed: [AUD-02]

coverage:
  - id: D1
    description: "Block-type screenshots + DOM measurements at 5 viewports captured as AUD-02 evidence"
    requirement: AUD-02
    verification:
      - kind: automated_ui
        ref: "playwright:baseline/screenshots/*.png (34 files) + baseline/measurements.json (103 boxes)"
        status: pass
    human_judgment: false
  - id: D2
    description: "AUD-02 visual-problem inventory written, grouped by block-type, each backed by DOM/axe evidence, with absent features flagged"
    requirement: AUD-02
    verification:
      - kind: manual_procedural
        ref: "grep AUD-02 + absent + header/hero/footer in 01-AUDIT.md (verify step passed)"
        status: pass
    human_judgment: true
    rationale: "Whether the enumerated problems are the right/complete problem set for Phases 2-5 is an editorial judgment reconciled against the contract in 01-04; automation only confirms structure + evidence citation, not completeness."

# Metrics
duration: ~25min
completed: 2026-06-25
status: complete
---

# Phase 1 Plan 03: AUD-02 Visual Problems by Block-Type Summary

**DOM-measured visual-problem inventory across 5 viewports — 9 block-type sections, P1 findings on form-input iOS-zoom (15px), consent/footer tap targets (36px/26px), hero line-height (170/150), 550px tablet title-bar; zero horizontal overflow site-wide; absent features (pricing/FAQ/modal) flagged net-new.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-06-25T20:30Z (approx)
- **Completed:** 2026-06-25T20:56Z
- **Tasks:** 2
- **Files modified:** 38 (.planning only — 34 PNG + 3 harness/data + 1 AUDIT.md)

## Accomplishments
- Captured 34 block-type screenshots and 103 DOM-measured boxes at the five locked viewports (1440/1024/768/390/360) via an ephemeral Playwright harness against the local static server — no site code touched, no-build honored.
- Wrote the AUD-02 section of 01-AUDIT.md: 9 block-type subsections (header/nav/hero/cards/forms/footer/title-bar/imagery/global) with what/where/viewport/why/screenshot tables, shared chrome audited once (no 11× duplication).
- Surfaced 4 P1 findings, all DOM-evidenced: form inputs 15px (iOS focus-zoom), consent label hit area 36px tall, footer menu links 26px tall (a documented 44px hit-zone that the live render does NOT apply — DOM-vs-CSS discrepancy), and the footer/global checks.
- Confirmed strong positives: zero horizontal overflow at all 5 viewports on both index and inner pages; gold footer border correct (`#ecab23`); burger/menu tap targets clear 44px; one-H1 semantics intact.
- Flagged absent features (pricing CNV-02, FAQ CMP-05, modal CMP-06) as net-new-or-descope, not audited as present.

## Task Commits

1. **Task 1: Capture DOM-measured screenshots at 5 viewports** - `c5a2a24` (feat)
2. **Task 2: Write AUD-02 visual-problems-by-block-type section** - `6202624` (docs)

**Plan metadata:** (this commit) (docs: complete plan)

## Files Created/Modified
- `baseline/measure.cjs` - Playwright harness: navigates representative pages at 5 viewports, records DOM boxes, writes screenshots + measurements.json
- `baseline/measure2.cjs` - Focused re-measure to disambiguate selector-misses (consent label, footer links, off-canvas, hero title) from real zero-size
- `baseline/measurements.json` - 103 DOM-measured boxes (block/page/viewport/metric/value)
- `baseline/screenshots/*.png` - 34 screenshots: header/nav-offcanvas/hero/cards/form/footer/titlebar × relevant viewports
- `01-AUDIT.md` - AUD-02 section filled (replaced the 01-01 placeholder)

## Decisions Made
- **DOM-measured over pixel-eyeballing:** Per project memory (`workflow-api-proxy-balance.md`), findings rest on measured boxes; screenshots are committed as corroborating evidence, not the primary source.
- **Force-add baseline/screenshots/:** The directory matches the generic `screenshots/` ignore (line 14, for ad-hoc Playwright junk), but the plan's `files_modified` and threat T-01-03 explicitly require these committed under `baseline/`. Force-added only this path; the generic rule stays intact so future ad-hoc shots remain ignored.
- **No axe IDs in findings:** AUD-01 is 0-violation across 11 pages, so the "fold axe violations into findings" instruction resolves to "none to fold" — explicitly stated in the section.

## Deviations from Plan
None - plan executed exactly as written. (The force-add of `baseline/screenshots/` is the documented commit mechanism for a plan-required artifact, not a scope deviation.)

## Issues Encountered
- **Playwright not resolvable from cwd:** No repo-local node_modules (no-build site). Resolved by requiring the globally-vendored `playwright@1.60.0` under `gsd-pi/node_modules` — same ephemeral-tooling approach the AUD-01 axe baseline used. Browsers already cached under `ms-playwright`.
- **Some first-pass selectors returned 0×0** (header wrapper height, off-canvas `#site-navigation`, footer link, hero `h2`): these were measurement-selector artifacts, not real defects. A focused `measure2.cjs` re-probe confirmed the real elements (e.g. footer links are 26px tall, hero `.pbmit-slider-title` is 170px). Zero-size artifacts were excluded from findings and noted as such.

## User Setup Required
None - no external service configuration required. (Static server `python -m http.server 8080` is started locally; no secrets, no network-exposed surface.)

## Next Phase Readiness
- AUD-02 inventory ready for plan **01-04** to reconcile findings against the UI-SPEC contract and feed the IMPL-PLAN (AUD-05).
- P1 findings (input zoom, consent/footer tap targets, footer DOM-vs-CSS hit-zone discrepancy) are the highest-value entries for Phase 2/5 to action.
- No blockers. The known mobile-header target-size flag remains an accepted documented exception (measured 44×44 this run).

## Self-Check: PASSED

- SUMMARY.md, 01-AUDIT.md (AUD-02 filled), measurements.json, measure.cjs — all FOUND
- 34 screenshots tracked under baseline/screenshots/
- Commits c5a2a24 (Task 1) and 6202624 (Task 2) — both FOUND in git log

---
*Phase: 01-baseline-audit-ui-design-contract*
*Completed: 2026-06-25*
