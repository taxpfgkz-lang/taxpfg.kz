---
phase: 01-baseline-audit-ui-design-contract
plan: 04
subsystem: planning-docs
tags: [audit, ui-contract, impl-plan, aud-04, aud-05]
dependency_graph:
  requires: ["01-01", "01-02", "01-03"]
  provides: ["01-UI-SPEC signed-off (AUD-04)", "01-IMPL-PLAN (AUD-05)"]
  affects: ["Phase 2", "Phase 3", "Phase 4", "Phase 5"]
tech_stack:
  added: []
  patterns: ["documents-only synthesis", "no site-code edits"]
key_files:
  created:
    - .planning/phases/01-baseline-audit-ui-design-contract/01-IMPL-PLAN.md
  modified:
    - .planning/phases/01-baseline-audit-ui-design-contract/01-UI-SPEC.md
decisions:
  - "01-UI-SPEC.md verified complete against AUD-04 (all six areas present) and Approval set pending -> approved; no re-authoring, only axe reconciliation + sign-off ticks"
  - "AUD-01 recorded 0 axe contrast violations -> no contrast gap to close in the contract; the WCAG AA floor already binds"
  - "Pricing (CNV-02), FAQ accordion (CMP-05), modal (CMP-06) marked NET-NEW, not polish; CMP-06 conditioned on Magnific Popup instantiation"
  - "Mobile header search target-size = accepted documented exception (WCAG 2.2 SC 2.5.8, outside scanned tag set); chart.js removal out-of-scope (v2/PERF-02)"
  - "!important budget carried forward as 57 functional / 59 grep-c, net-new ~= 0 Phase-2 gate"
metrics:
  duration: "~14m"
  completed: 2026-06-26
status: complete
---

# Phase 1 Plan 04: Contract Sign-Off + Implementation Plan Summary

Verified the already-approved UI design contract (01-UI-SPEC.md) complete against AUD-04 and signed it off, then wrote the AUD-05 implementation plan (01-IMPL-PLAN.md) sequencing the Phase 2–5 file changes — a documents-only phase that locks the rules and the work-order before any code is written.

## What Was Built

**Task 1 — AUD-04 contract verification + sign-off** (`01-UI-SPEC.md`, commit `b567359`):
- Confirmed the contract already contains all six AUD-04 areas (design tokens, 4px spacing scale, fluid type scale, color+contrast floor, component-state contract, hard constraints) — no re-authoring needed.
- Reconciled the contrast floor against 01-AUDIT.md: AUD-01 recorded **0 axe contrast violations** across 11 pages, so there was **no gap to close**. Added an explicit "Axe reconciliation" note recording this and binding Phase 5 to keep axe contrast at 0.
- Marked the five "Open Questions" resolved, each with a pointer to where it was answered (font-loading → RESEARCH Q1/v2 PERF-03; img inventory → RESEARCH Q2 + AUD-02 I1/I2; pricing/FAQ/modal absence → RESEARCH Q3 + AUD-02 absent-features; chart.js → RESEARCH Q4 + CONFLICT-CATALOG; target-size → AUD-01 H2).
- Ticked all 6 Checker Sign-Off dimensions and set **Approval: pending → approved (2026-06-25)**. No locked decision weakened.

**Task 2 — AUD-05 implementation plan** (`01-IMPL-PLAN.md`, commit `976eeaf`):
- **File-change order** section maps each downstream phase to the files it edits (`custom.css`/`base.css`/`custom.js`) and why, in dependency order: Phase 2 (token sheet + spacing/type scale, root dependency) → Phase 3 (components, needs P2 tokens; `custom.js` a11y patches only) → Phase 4 (conversion blocks + imagery, needs stable components; `custom.js` for sticky-CTA↔WhatsApp collision) → Phase 5 (focus/motion polish + verification run). Each phase lists the specific AUD-02 findings it lands.
- **Net-new vs polish** section: pricing (CNV-02), FAQ (CMP-05), modal (CMP-06) marked NET-NEW features to be built in full (no scope-reducing language); CMP-06 conditioned on Magnific Popup actually being instantiated. Target-size flag = accepted documented exception; chart.js, image payload, font-loading, header/footer templating all marked out-of-scope (v2).
- **Carried gates** section: the `!important` budget (57 functional / 59 grep-c, net-new ≈ 0); the recurring per-phase verification gate (multi-breakpoint DOM-measured Playwright + axe-0-new + JS smoke + change-all-11 grep); the AUD-01 regression floor (a11y ≥ 95, axe = 0) Phase 5 measures against.

## Deviations from Plan

None — plan executed exactly as written. Both tasks `type="auto"`; no checkpoints, no auth gates, no architectural decisions. The only legitimate edit to the contract (an axe-gap closure) was not needed because AUD-01 had 0 contrast violations; the change was limited to a reconciliation note + sign-off ticks, as the plan allowed.

## Verification

- Task 1 automated check: `grep` for `approved` + `Hard Constraints` + `spacing scale` in 01-UI-SPEC.md → **PASS**.
- Task 2 automated check: `grep` for `file-change order` + `net-new` + `custom.css` + `out of scope` in 01-IMPL-PLAN.md → **PASS**.
- `git status` scope: the two commits touched only `.planning/` documents. No `css/*`, `js/*`, or `*.html` edits were made by this plan. (Pre-existing unrelated working-tree changes to root HTML and `docs/*` were present at conversation start and were left untouched — not part of this plan's commits.)

## Self-Check: PASSED

- FOUND: `.planning/phases/01-baseline-audit-ui-design-contract/01-UI-SPEC.md`
- FOUND: `.planning/phases/01-baseline-audit-ui-design-contract/01-IMPL-PLAN.md`
- FOUND commit: `b567359` (Task 1)
- FOUND commit: `976eeaf` (Task 2)
