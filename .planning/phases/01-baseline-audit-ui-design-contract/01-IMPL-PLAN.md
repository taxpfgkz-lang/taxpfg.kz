# 01-IMPL-PLAN — Implementation Plan (AUD-05)

- **Milestone:** v1.0 — taxpfg.kz Production UI Polish
- **Phase:** 01 — baseline-audit-ui-design-contract
- **Plan:** 01-04 (AUD-05)
- **Date:** 2026-06-26
- **Status:** final

## Purpose

This document states **which files change in Phases 2–5, why, and in what order** so the
downstream phases execute deterministically against a frozen contract. It is the AUD-05
deliverable and the work-order companion to the AUD-04 design contract.

It **consumes** three Phase-1 artifacts and adds nothing new to them:

- **01-CONFLICT-CATALOG.md (AUD-03)** — the `!important` override budget (57 functional
  declarations / 59 grep-c line count) and the hard do-not-touch boundary (`swiper-*`,
  `data-aos*`, `pbmit-*`, load-order, off-canvas-safe).
- **01-AUDIT.md (AUD-01 + AUD-02)** — the regression floor (a11y ≥ 95, axe = 0) and the
  visual-problem inventory by block-type (the "what to fix"), every finding DOM-measured at
  1440 / 1024 / 768 / 390 / 360.
- **01-UI-SPEC.md (AUD-04)** — the binding tokens, spacing scale, type scale, color+contrast
  floor, component-state contract, and Hard Constraints every change below must honor.

**Editable file set (vendor-read-only boundary):** only `css/custom.css`, `css/base.css`,
and `js/custom.js` may be edited. All other `css/*` and `js/*` are theme-owned and read-only
(`custom.css:1-4`, `js/custom.js:113-130`, CLAUDE.md). `custom.css` stays the **last**
stylesheet and `custom.js` the **last** script across all 11 pages, or the cascade overrides
and post-init DOM patches stop working (load-order constraint).

---

## File-change order

Phases run bottom-up in dependency order: tokens everything inherits → components built on
tokens → conversion composites built on stable components → final a11y/verification proof.
Each phase below lists the **files it edits**, the **why**, and the **AUD-02 findings / UI-SPEC
sections it lands**.

### Phase 2 — Design Tokens + Primitives (TOK-01, TOK-02, TOK-03, VIS-02, VIS-03)

| File | Edit | Why |
|------|------|-----|
| `css/custom.css` | **Primary.** Consolidate the `:root` `--pfg-*` token sheet (ink+gold palette, radii, shadows, transitions, z-index per TOK-01); declare the 4px `--pfg-space-*` spacing scale (TOK-02) and the fluid `clamp()` type scale (TOK-03); snap existing section paddings to the nearest token; apply `text-wrap: balance/pretty` + Russian non-breaking rules; darken any sub-AA body/gold text to `--pfg-gold-ink` (VIS-03). | This is the **root dependency** — every component and conversion block inherits these tokens. Nothing composes until the token sheet, spacing scale, and type scale land. `custom.css` is loaded last so the consolidated `:root` wins by source-order. |
| `css/base.css` | **Only if needed** — touch a `--pbmit-*` vendor token solely to *reference* or surgically override a brand value the `--pfg-*` layer must reuse (the token namespaces live at `base.css:21-49`). Prefer reading the vendor token via `var()` from `custom.css` over editing `base.css`. | Vendor tokens are the source of truth for brand color/typography; `custom.css` should reuse them via `var()`. Editing `base.css` is the exception, not the default. |
| `js/custom.js` | **No edit in Phase 2.** | Phase 2 is pure CSS token/scale work; no behavior or a11y patch is in scope here. |

**Lands these AUD-02 findings:** HE1 / T2 / G2 (heading line-height normalization — no `clamp()`
heading sits below lh 1.0), C1 (card padding 28px → snap to `--pfg-space-6`/`-8`), F1 (mobile
input font-size 15px → ≥16px to stop iOS focus-zoom — token/scale-driven), the spacing-rhythm
snapping notes across section paddings.

### Phase 3 — Components (VIS-01, CMP-01..CMP-06)

| File | Edit | Why |
|------|------|-----|
| `css/custom.css` | **Primary.** Style the `.pfg-*` component rules + targeted `pbmit-*` overrides: button primary/secondary/ghost hierarchy with hover/focus-visible/active/disabled (CMP-01); form rest/focus/error/success (CMP-02); service-card rest/hover-lift (CMP-03); nav sticky-header + off-canvas states (CMP-04); **net-new** FAQ accordion (CMP-05) and modal styling (CMP-06, conditional — see Net-new section). Add the central visual system so headings/CTAs/cards read consistently across 11 pages (VIS-01). | Needs the Phase-2 tokens to exist first — components are styled *with* the spacing/type/color tokens, not with hardcoded values. |
| `js/custom.js` | **a11y / ARIA patches only — no behavior change.** Add correct ARIA + keyboard handling for the net-new FAQ accordion (CMP-05) and, if instantiated, modal focus-trap (CMP-06); patch any missing `aria-*` on existing controls. Follow the existing `initX()` guard-and-early-return + idempotent-patch pattern. Form→WhatsApp behavior stays byte-identical (CMP-02, VER-04). | The theme JS owns widget init; `custom.js` only adds the a11y layer the theme lacks. Behavior (form flow, marquee, slider, analytics) must not change. |

**Lands these AUD-02 findings:** FT1 (footer menu links 26px tall → reconcile the 44px
hit-zone selector that the live render does not apply), N1/N2 (document desktop-nav scope
≥1201px; tap targets already healthy), F2 (consent label hit area 36px tall → ≥44px).
**Do-not-touch reminder:** style by adding `.pfg-*` / overriding `pbmit-*` via cascade — never
rename or remove `swiper-*`, `data-aos*`, or `pbmit-*` hooks; no `filter`/`transform`/
`backdrop-filter` on off-canvas-menu ancestors.

### Phase 4 — Conversion Blocks + Imagery (CNV-01..CNV-04, IMG-01)

| File | Edit | Why |
|------|------|-----|
| `css/custom.css` | **Primary.** Hero value-prop + single primary CTA + above-fold trust signals (CNV-01); **net-new** pricing block with one "популярный" highlight + per-tier CTA (CNV-02); site-wide CTA hierarchy (CNV-03); footer parity across 11 pages (CNV-04); imagery sizing/proportion consistency (IMG-01, presentation only). | Needs **stable components** from Phase 3 — conversion blocks are composites of the Phase-3 buttons/cards/forms. |
| `js/custom.js` | **Sticky-CTA ↔ floating-WhatsApp collision resolution only (CNV-03).** Resolve the mobile sticky-CTA vs `.pfg-whatsapp-float` overlap (fold WhatsApp into the bar, or offset/hide one when the other is in view) — a small design spike per ROADMAP P4. No other behavior change. | This is the one conversion interaction that needs JS; everything else in P4 is CSS. The reconciliation must never ship the two controls overlapping. |

**Lands these AUD-02 findings:** HE1/HE2 (hero line-height + height/LCP polish — visual, perf
not a gate), T1 (title-bar 550px band on 768 → add a smaller min-height tier between 768 and
390), I1/I2 (imagery sizing — bulk WebP/AVIF re-encode is **v2/PERF-01, out of scope**;
presentation/sizing only here), FT3 (footer vertical density on mobile — low priority).
**Footer is shared chrome** → any footer markup touch is a change-all-11 edit (grep returns 11)
in one atomic commit.

### Phase 5 — Accessibility Pass + Cross-Device Verification (A11Y-01..04, VER-01..04)

| File | Edit | Why |
|------|------|-----|
| `css/custom.css` | Focus-visible polish (ensure every interactive element keeps a visible ring, no bare `outline:none` — A11Y-01); confirm all new decorative motion sits inside the scoped `prefers-reduced-motion` block (`custom.css:332-345`) without touching the brand-motion floor (A11Y-03). | Final a11y hardening layered on the now-complete component + conversion work. |
| `js/custom.js` | Only if a final ARIA/focus gap is found during verification; otherwise read-only. | Verification phase — proof, not new feature work. |
| *(verification run — no file edit)* | DOM-measured Playwright @ 1440/1024/768/390/360, Lighthouse + axe across all 11 pages, JS smoke test, before/after screenshots, local-check command list (VER-01..03), behavior-diff smoke (VER-04). | Proves a11y ≥ the AUD-01 floor and that business logic is byte/behavior-identical. |

**Measured against:** the AUD-01 regression floor — a11y ≥ 95 every page, axe = 0 for the
scanned tag set, no horizontal overflow, ≥44px targets, headings not clipped.

---

## Net-new vs polish

The audit confirmed three requirements have **no existing UI on any of the 11 pages**
(01-AUDIT "Absent features", 01-RESEARCH Q3). These are **net-new features to be built in
full** in their phase — they are *not* "polish existing UI", and they must be delivered
completely (no scope-reducing "v1/placeholder/static-for-now" framing).

| Feature | Requirement | Phase | Disposition |
|---------|-------------|-------|-------------|
| Pricing / tariff block | **CNV-02** | Phase 4 | **NET-NEW.** Zero `pricing`/`тариф`/`price-table` markup exists today — build the packages presentation with exactly one "популярный" highlight and a per-tier CTA, in full. |
| FAQ accordion | **CMP-05** | Phase 3 | **NET-NEW.** No `.accordion` markup instantiated (theme handler exists at `js/scripts.js:309` but no page uses it) — build the accordion with correct ARIA + keyboard, in full. |
| Live modal / lightbox | **CMP-06** | Phase 3 | **NET-NEW, CONDITIONAL.** Magnific Popup is loaded on all 11 pages but **zero** markup triggers it. CMP-06 modal rules proceed **only if Magnific Popup is actually instantiated** — confirm instantiation at the start of Phase 3 before writing any modal rule (UI-SPEC already gates this). If never instantiated, CMP-06 is descoped, not faked. |

**Accepted documented exception (not work):**

- **Mobile header search target-size** — theme-owned control, measured 44×44 px in AUD-01 (did
  not surface as a hard blocker); maps to WCAG 2.2 SC 2.5.8, outside the scanned
  `wcag2a/2aa/21a/21aa` axe tag set. Carried as a **standing accepted exception** per MEMORY
  `ui-audit-2026-06-23` and RESEARCH Open Question 2 — **not** scheduled work in any phase.

**Out of scope (v2):**

- **chart.js removal** — `js/chart.js` (Chart.js 4.5.0) is vendored but referenced by zero
  pages (zero runtime cost; dead repo weight only). Removal is **OUT OF SCOPE for v1.0 →
  deferred to v2 / PERF-02**. Leave the file in place; do not "discover" and act on it this
  milestone.
- **Image payload optimization** (WebP/AVIF, `srcset`, `loading=lazy`, `<picture>`) — **v2 /
  PERF-01**. Phase-4 IMG-01 is presentation/sizing only.
- **Font-loading optimization** (`font-display`, preload) — **v2 / PERF-03**.
- **Header/footer templating** (de-duplicate the 11-page chrome) — **v2 / MNT-01** (would
  require a build system, which the project deliberately avoids).

---

## Carried gates

These gates are carried forward from Phase 1 and the ROADMAP P2–P5 notes, and apply to every
downstream phase that edits code.

### `!important` budget (Phase-2 net-new ≈ 0 floor)

- **Baseline = 59** (`grep -c '!important' css/custom.css`) / **57 functional declarations**
  (3 of the 59 lines are Russian comment-prose at lines 317/643/644 — see 01-CONFLICT-CATALOG
  count reconciliation).
- **Net-new ≈ 0:** Phase 2 may relocate or consolidate existing overrides but must **not grow**
  the count. Every new `!important` (any phase) must **cite the vendor rule it beats** in a
  Russian comment. 31 of the 57 existing declarations are currently **uncited** — Phase 2 must
  confirm the actual beaten vendor selector before relocating or dropping them.
- **No `@layer`** — unlayered vendor always beats layered; win by source-order + targeted
  specificity only.

### Recurring per-phase verification gate (ROADMAP P2–P5)

Definition-of-done for every code phase includes:

- **DOM-measured Playwright** @ 1440 / 1024 / 768 / 390 / 360: no horizontal scroll, ≥44px tap
  targets, headings not clipped (trust the rendered box, not `custom.css` source text).
- **axe / Lighthouse 0-new-violations** vs the Phase-1 baseline.
- **JS smoke test:** menu / WhatsApp float / lead-form→WhatsApp / marquee / slider /
  reduced-motion all still work (behavior byte/behavior-identical — VER-04).
- **change-all-11 grep** (returns 11) wherever shared chrome markup is touched.
- **Do-not-touch boundary** held: no rename/removal of `swiper-*`, `data-aos*`, `pbmit-*`; no
  `filter`/`transform`/`backdrop-filter` on off-canvas-menu ancestors; `custom.css` last
  stylesheet, `custom.js` last script.

### AUD-01 regression floor (Phase 5 acceptance)

- **a11y ≥ 95** on every page (the minimum across the 11; index/services/contacts = 96), **axe
  = 0** for the scanned `wcag2a/2aa/21a/21aa` tag set. Phase 5 (A11Y-04, VER-01) is measured
  against these committed numbers — no later phase may drop any page below its AUD-01 row value.
- Performance (55–57) is recorded for reference but is **not** a regression gate this milestone.

---

## Verification (read-only confirmation)

- `git status` shows changes only under `.planning/` — no edits to `css/*`, `js/*`, or
  `*.html` (this is a documents-only phase).
- This plan consumes 01-CONFLICT-CATALOG.md, 01-AUDIT.md, and 01-UI-SPEC.md; it introduces no
  new findings or decisions beyond sequencing them.
