# Roadmap: taxpfg.kz — Production UI Polish

## Overview

This is a brownfield visual hardening of a live, no-build static marketing site (11 pages, GudFin/PBMIT theme + Bootstrap 5.2 + a thin `pfg-*` override layer). The journey is strictly bottom-up: first capture the regression floor and lock the rules (audit + design contract, code-frozen), then build the design-token foundation everything inherits, then style reusable components, then tune the conversion composites and imagery, and finally run a dedicated accessibility pass and cross-device verification proving nothing regressed. Every edit lives only in `css/custom.css`, `css/base.css`, and `js/custom.js`; vendor/theme files stay read-only; business logic (form→WhatsApp, analytics, routing, JSON-LD, brand animations) stays byte/behavior-identical.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Baseline Audit + UI Design Contract** - Capture the Lighthouse/axe floor and lock the rules before any code changes (documents only) (completed 2026-06-25)
- [x] **Phase 2: Design Tokens + Primitives** - Consolidate the `:root` token sheet, spacing scale, and fluid type scale everything inherits (completed 2026-06-25)
- [ ] **Phase 3: Components** - Style buttons, forms, cards, nav, FAQ, and modals with all interaction states
- [ ] **Phase 4: Conversion Blocks + Imagery** - Tune hero, pricing, CTA hierarchy, footer parity, and imagery; resolve the sticky-CTA vs WhatsApp collision
- [ ] **Phase 5: Accessibility Pass + Cross-Device Verification** - Prove a11y ≥ baseline across all 11 pages at every breakpoint with logic untouched

## Phase Details

### Phase 1: Baseline Audit + UI Design Contract

**Goal**: Capture the regression floor and lock every design rule before a single byte of code changes. This phase produces DOCUMENTS, not code edits — the customer's hard audit-first requirement.
**Depends on**: Nothing (first phase)
**Requirements**: AUD-01, AUD-02, AUD-03, AUD-04, AUD-05
**Success Criteria** (what must be TRUE):

  1. Per-page Lighthouse + axe baseline (a11y/perf/CLS) is recorded for all 11 pages as the "не хуже" floor (AUD-01 — the dependency gate for all later verification).
  2. UI audit report enumerates visual problems with what/where/why across desktop/tablet/mobile.
  3. Conflict catalog documents the `custom.css` ↔ vendor `!important` ledger (~59 baseline) plus the do-not-touch theme class/attribute list (`swiper-*`, `data-aos*`, `pbmit-*`).
  4. UI design contract fixes tokens, spacing scale, type scale, color+contrast, component states/rules, and hard constraints (visual-only, vendor read-only, no `@layer`, focus-always, scoped-motion).
  5. Implementation plan states which files (`custom.css`/`base.css`/`custom.js`) change, why, and in what order.

**Plans**: 1/4 plans executed
**Wave 1**

- [x] 01-01-PLAN.md — AUD-01 Lighthouse + axe baseline (regression floor) for all 11 pages
- [x] 01-02-PLAN.md — AUD-03 !important ledger (59) + do-not-touch namespaces + chart.js disposition

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-03-PLAN.md — AUD-02 visual-problem inventory by block-type (DOM-measured, 5 viewports)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-04-PLAN.md — AUD-04 contract verification/sign-off + AUD-05 implementation plan

**Notes**: No code edits in this phase, so the recurring implementation gate does not apply. AUD-01 baseline numbers become the regression floor that Phase 5 (A11Y-04, VER-01) is measured against. Resolve open questions from research/SUMMARY.md here (live `<head>` font-loading config; `<img>` vs CSS-background asset inventory; which pages have pricing/FAQ/modal; whether `chart.js` deletion stays out).
**UI hint**: yes

### Phase 2: Design Tokens + Primitives

**Goal**: A single design-token foundation everything downstream inherits — consolidated `:root` palette, a token-based spacing scale, and a fluid type scale. This is the root dependency: components and conversion blocks will not compose until it lands.
**Depends on**: Phase 1
**Requirements**: TOK-01, TOK-02, TOK-03, VIS-02, VIS-03
**Success Criteria** (what must be TRUE):

  1. A `:root` token sheet in `custom.css` consolidates the ink+gold palette, radii, shadows, transitions, and z-index (TOK-01); `custom.css` stays last in load order.
  2. Section/block spacing follows one token-based spacing scale with no broken gaps, and alignment/grid is consistent across pages (TOK-02, VIS-02).
  3. Headings and body text use a `clamp()` fluid type scale with correct line-height and no harsh Russian wrapping (`text-wrap: balance/pretty`, orphan guard) (TOK-03).
  4. Colors and contrast meet WCAG AA: gold text uses the `--pfg-gold-ink` token (≥5.4:1), and the gold fill is never used as low-contrast body text on white (VIS-03).

**Plans**: 1/2 plans executed

**Wave 1**

- [x] 02-01-PLAN.md — TOK-01/02/03 declaration: extend `:root` with `--pfg-space-*`, fluid `--pfg-fs-*`/`--pfg-lh-*`, `--pfg-z-float`

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-02-PLAN.md — TOK-02/03 + VIS-02/03 application: card-padding snap, F1 input 16px, line-height policy, text-wrap, contrast guard + DOM/axe/JS-smoke verify

**Notes**: Definition-of-done includes the recurring gate — DOM-measured Playwright check at 1440/1024/768/390/360 (no horizontal scroll, ≥44px targets, headings not clipped); axe/Lighthouse 0-new-violations vs the Phase-1 baseline; JS smoke test (menu/WhatsApp/form/marquee/slider/reduced-motion); change-all-11 grep (returns 11) where any shared markup is touched; `!important` net-new ≈ 0 with each new one citing the vendor rule it beats. No `@layer` — unlayered source-order + targeted specificity only.
**UI hint**: yes

### Phase 3: Components

**Goal**: Every reusable component renders systemically with all interaction states, so the same look reaches all 11 pages via the central token layer.
**Depends on**: Phase 2
**Requirements**: VIS-01, CMP-01, CMP-02, CMP-03, CMP-04, CMP-05, CMP-06
**Success Criteria** (what must be TRUE):

  1. Buttons share a primary/secondary/ghost hierarchy with hover/focus/active/disabled states and readable contrast (CMP-01).
  2. Forms and inputs have visible labels, focus/error/success states, and correct mobile keyboards — and the form→WhatsApp behavior is unchanged (CMP-02).
  3. Service cards, navigation (sticky header + mobile off-canvas menu), the FAQ accordion, and modals (if Magnific Popup is instantiated) render consistently with correct ARIA and focus management, without breaking theme JS (CMP-03, CMP-04, CMP-05, CMP-06).
  4. Headings, subheadings, CTAs, blocks, and cards read as one visual system across all 11 pages (VIS-01).

**Plans**: TBD
**Notes**: Research flag YES — enumerate per-page component coverage (which pages have pricing/FAQ/modal) by walking each page, and confirm Magnific Popup is actually instantiated before writing modal rules. Recurring gate applies in full (multi-breakpoint DOM-measured Playwright + axe 0-new + JS smoke + change-all-11 grep + behavior-diff guard + `!important` budget). Style by adding `.pfg-*` classes; never rename/remove theme JS hooks; no `filter`/`transform`/`backdrop-filter` on off-canvas-menu ancestors.
**UI hint**: yes

### Phase 4: Conversion Blocks + Imagery

**Goal**: The conversion composites convert cleanly and imagery is consistent — built on stable components from Phase 3.
**Depends on**: Phase 3
**Requirements**: CNV-01, CNV-02, CNV-03, CNV-04, IMG-01
**Success Criteria** (what must be TRUE):

  1. Hero shows a clear value-prop, a single prominent primary CTA, and trust signals above the fold (CNV-01).
  2. Pricing tiers read clearly with exactly one "популярный" highlight and a per-tier CTA (CNV-02).
  3. Site-wide CTAs have a strong, uncluttered visual hierarchy, and the sticky-mobile-CTA vs floating-WhatsApp collision is deliberately resolved — never shipped overlapping (CNV-03).
  4. The footer is unified and credibility-oriented, identical across all 11 pages (CNV-04).
  5. Images and icons share a consistent style with correct sizes and proportions and no visual junk (IMG-01).

**Plans**: TBD
**Notes**: Research flag YES — the sticky-CTA/WhatsApp reconciliation and pricing-tier layout need a small design spike (fold WhatsApp into the bar, or offset/hide one when the other is in view). Footer is shared chrome → change-all-11 grep (returns 11) + multi-page screenshot diff in one atomic commit. Recurring gate applies in full. Image work here is presentation/sizing only — payload/WebP optimization is a deferred v2 milestone.
**UI hint**: yes

### Phase 5: Accessibility Pass + Cross-Device Verification

**Goal**: Prove the integrated result meets the a11y floor across every device and breakpoint, with business logic provably untouched.
**Depends on**: Phase 4 (and Phase 1 for the AUD-01 baseline floor)
**Requirements**: A11Y-01, A11Y-02, A11Y-03, A11Y-04, VER-01, VER-02, VER-03, VER-04
**Success Criteria** (what must be TRUE):

  1. Every interactive element has a visible keyboard `:focus-visible` indicator (no bare `outline:none`), and ARIA is correct on nav/accordion/forms/modals with AA-contrast readable text (A11Y-01, A11Y-02).
  2. New decorative motion lives inside the scoped `prefers-reduced-motion` block; brand motion (Swiper/marquee/GSAP) floor stays intact (A11Y-03).
  3. Lighthouse/axe accessibility is ≥ the AUD-01 baseline on all 11 pages, DOM-measured via Playwright at 1440/1024/768/390/360 (no horizontal scroll, ≥44px targets) (A11Y-04, VER-01).
  4. A final before/after UI review with screenshots and a local-check command list (static server, Lighthouse, axe, Playwright run) is delivered (VER-02, VER-03).
  5. A smoke test confirms business logic, form→WhatsApp message + number, analytics, routing, JSON-LD, and animations are byte/behavior-identical (VER-04).

**Plans**: TBD
**Notes**: This phase exercises the drift-audit script across all 11 pages and consolidates the recurring per-phase gates into the final acceptance run. Verification is measured against the Phase-1 baseline (hard dependency). The known mobile header search target-size flag is an accepted documented exception, not a new violation.
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Baseline Audit + UI Design Contract | 4/5 | Complete    | 2026-06-25 |
| 2. Design Tokens + Primitives | 2/2 | Complete    | 2026-06-25 |
| 3. Components | 0/TBD | Not started | - |
| 4. Conversion Blocks + Imagery | 0/TBD | Not started | - |
| 5. Accessibility Pass + Cross-Device Verification | 0/TBD | Not started | - |
