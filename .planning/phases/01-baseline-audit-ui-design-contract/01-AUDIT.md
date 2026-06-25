# Phase 01 — Baseline Audit & UI Design Contract — AUDIT

**Milestone:** v1.0 — taxpfg.kz Production UI Polish
**Audit date:** 2026-06-26
**Tooling:**
- Lighthouse `13.4.0` (categories: performance, accessibility; Chrome `--headless=new`)
- `@axe-core/playwright` `4.12.1` (axe-core engine `4.12.1`; tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`)
- Served via `python -m http.server 8080` (bound `127.0.0.1`) from the repo root — all audits ran over `http://127.0.0.1:8080/<page>`, never `file://`, so relative `css/js`, `@import` Google Fonts and the Maps iframe resolved and metrics are accurate (RESEARCH Pitfall 4).

**Regression floor statement:** The numbers in the AUD-01 table below are the committed regression floor for **AUD-01**. This is the dependency gate that Phase 5 (A11Y-04, VER-01) is measured against — no later phase may drop a page's accessibility score below the floor recorded here. Raw reports are committed under `baseline/lighthouse/` (11 JSON + 11 HTML) and `baseline/axe/` (11 JSON).

## AUD-01 — Per-page baseline

| Page | A11y score | Perf score | CLS | LCP (ms) | axe violations | axe critical/serious IDs |
|------|-----------:|-----------:|----:|---------:|---------------:|--------------------------|
| index.html               | 96 | 55 | 0.077 | 15392 | 0 | none |
| about.html               | 95 | 57 | 0.000 |  9158 | 0 | none |
| services.html            | 96 | 56 | 0.000 | 10070 | 0 | none |
| accounting.html          | 95 | 56 | 0.000 |  9924 | 0 | none |
| accounting-recovery.html | 95 | 56 | 0.000 |  9768 | 0 | none |
| taxes.html               | 95 | 56 | 0.000 |  9920 | 0 | none |
| consulting.html          | 95 | 56 | 0.000 |  9928 | 0 | none |
| registration.html        | 95 | 56 | 0.000 |  9761 | 0 | none |
| contacts.html            | 96 | 56 | 0.000 |  9996 | 0 | none |
| privacy.html             | 95 | 56 | 0.000 |  9760 | 0 | none |
| 404.html                 | 95 | 56 | 0.000 |  9779 | 0 | none |

**Floor note:**
- **Minimum accessibility score across the 11 pages = 95** (all content pages except `index.html`, `services.html`, `contacts.html` which score 96). No later phase may drop any page below its row value here; the hard a11y floor is **95**.
- **axe-core (WCAG 2.0/2.1 A + AA): zero violations on all 11 pages.** This is a clean WCAG floor — Phase 5 must keep it at zero for the scanned tag set.
- **Performance** sits at 55–57 across the board. This is *not* a regression gate for this milestone (the milestone is UI polish, not perf), but it is recorded for reference. `index.html` LCP (~15.4 s) is the outlier (hero slider); all inner pages cluster ~9–10 s. CLS is effectively 0 everywhere except `index.html` (0.077, still within Lighthouse "good" < 0.1).

### Known accepted exception (not a new violation)

The previously documented **mobile header search target-size** flag (theme-owned, accepted exception per RESEARCH Open Question 2 and MEMORY `ui-audit-2026-06-23`) did **not** surface in this axe run because it maps to **WCAG 2.2 SC 2.5.8 (Target Size, Minimum)**, which is outside the `wcag2a/2aa/21a/21aa` tag set scanned here. It is therefore not counted in the 0-violation floor above. Plan 01-03 should log it as a standing exception rather than new work, unless it surfaces as a hard blocker.

### Reproduce

```bash
# from repo root
python -m http.server 8080 --bind 127.0.0.1   # one shell

# Lighthouse (per page; <slug> = filename without .html, 404 for 404.html)
npx -y lighthouse@13.4.0 http://127.0.0.1:8080/<slug>.html \
  --output=json --output=html \
  --output-path=.planning/phases/01-baseline-audit-ui-design-contract/baseline/lighthouse/<slug> \
  --only-categories=performance,accessibility --chrome-flags="--headless=new"

# axe-core via @axe-core/playwright 4.12.1 (ephemeral runner; tags wcag2a/2aa/21a/21aa)
```

> Windows/Cyrillic-path note: Lighthouse prints a non-fatal `EPERM ... rmSync` at temp **cleanup** (`chrome-launcher destroyTmp`) *after* the report is already saved. The JSON/HTML reports are complete and valid; the error is cosmetic temp-dir teardown only.

## AUD-02 — Visual problems by block-type

**Method:** Findings are grouped by **block-type**, not by page — shared chrome (header/nav/footer/form/title-bar is copy-pasted into all 11 HTML files, RESEARCH Pattern 1) is audited **once** with page-specific deltas noted, so an identical header finding is not repeated 11×. Every "Why" cites a **DOM-measured value** taken from the live render at the stated viewport (RESEARCH Pattern 2 + Pitfall 5: trust the rendered box, not `custom.css` source text), or an axe rule ID. Measurements come from `baseline/measurements.json` (103 boxes) captured via the ephemeral Playwright harness `baseline/measure.cjs` / `measure2.cjs` against `http://127.0.0.1:8080` at the five locked viewports **1440 / 1024 / 768 / 390 / 360**. Screenshots are under `baseline/screenshots/<block>-<vw>.png`.

**axe note:** AUD-01 recorded **zero** axe violations (`wcag2a/2aa/21a/21aa`) on all 11 pages. There are therefore **no axe rule IDs to fold into these findings** — every AUD-02 finding rests on a DOM measurement. The known mobile-header target-size flag maps to **WCAG 2.2 SC 2.5.8**, outside the scanned tag set (see "Accepted documented exceptions" below).

**Representative pages** (Claude's Discretion per CONTEXT.md): `index.html` (hero/slider + imagery), `services.html` (title-bar + service cards), `contacts.html` (lead form + map + footer), `about.html` (shared header/nav). Screenshot refs name the block + viewport.

**Severity legend:** P1 = visible defect / a11y tap-target or zoom issue; P2 = noticeable polish/rhythm gap; P3 = minor / token-snapping nicety.

### Header (shared chrome — all 11 pages)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| H1 | Logo does not scale down on small phones; fixed-width text logo eats most of the bar | `.pfg-logo` (header, all pages) | 390, 360 | Logo box measured **249×31 px at every viewport** incl. 360 (no responsive shrink) → ~69% of a 360px viewport. No overflow (see G1) but leaves the burger crowded. | `header-360.png`, `header-390.png` | P3 |
| H2 | Mobile header search control — known target-size flag | theme search toggle (header) | 390, 360 | Measured hit box **44×44 px** this run (passes WCAG 2.5.5 AAA & 2.5.8 AA 24px). Did **not** surface as a hard blocker. Recorded as **accepted documented exception**, not new work. | `header-390.png` | — |

### Navigation — sticky desktop menu + off-canvas (shared chrome)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| N1 | Off-canvas menu trigger appears earlier than "tablet"; horizontal menu is gated to ≥1201px so 1025–1200px also gets the burger | menu toggle / `#site-navigation` | 1024, 768 | At 1024 & 768 the burger is **visible 55×55 px** and the inline menu is suppressed; horizontal nav only at ≥1201 (glass-header gate, CONTEXT). Not a defect — documents the breakpoint so the contract's "desktop nav" rules are scoped ≥1201, not ≥1024. | `header-1024.png`, `nav-offcanvas-1024.png` | P3 |
| N2 | Burger and off-canvas link tap targets are healthy | menu toggle, off-canvas links | 1024→360 | Burger **55×55** (1024/768), **45×45** (390/360); first menu link **109×47** — all clear the 44px floor. Positive finding (no fix needed). | `nav-offcanvas-390.png` | — |

> Off-canvas panel: clicking the toggle sets `body.active.pfg-menu-open` (confirmed via DOM) and the panel renders in `nav-offcanvas-*.png`. The theme's `#site-navigation` wrapper itself measures 0×0/`visibility:hidden` (the visible panel is a theme-managed sibling) — this is a **measurement selector artifact, not a finding**.

### Hero / Slider (index.html only)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| HE1 | Slider headline `line-height` is **smaller than** `font-size` on desktop → ascender/descender clipping risk on multi-line or tall-cap Cyrillic | `.pbmit-slider-title` / `.swiper-slide h2` | 1440 (and 1024 scaled) | Measured **font-size 170px, line-height 150px** (lh < fs) at 1440. On a two-line Russian headline the lines overlap vertically. Mobile is fine (390: **42.9px / 48px**, ratio ~1.12). | `hero-1440.png`, `hero-390.png` | P2 |
| HE2 | Hero is very tall and is the page's LCP/CLS outlier | `.pbmit-slider-area` | 1440, 1024 | Hero box **1000px tall at 1440**, 700px at 1024. AUD-01: index LCP **≈15.4 s** (slowest page) and the only page with **CLS 0.077** — both attributable to the slider. Perf is not a regression gate this milestone, but the visual height + load cost are noted for hero polish (VIS scope). | `hero-1440.png`, `hero-1024.png` | P2 |
| HE3 | Hero/`<h1>` semantics correct | visually-hidden `<h1 class="pfg-sr-only">` | all | Confirmed `srH1 = "Бухгалтерское сопровождение ИП и ТОО в А…"` present; slider uses `h2`. Positive finding — matches contract (exactly one H1). | — | — |

### Service cards (services.html; pattern shared by inner pages)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| C1 | Card padding is off the 4px spacing scale | `.pfg-card` / service box | all | Measured **padding 28px** at every viewport. Nearest scale tokens are **24 (`--pfg-space-6`) or 32 (`--pfg-space-8`)** — 28 snaps to neither. Token-snapping note for TOK-02 (snap to nearest, preserve rhythm). | `cards-1440.png`, `cards-390.png` | P3 |
| C2 | Minor card-height jitter between adjacent breakpoints | `.pfg-card` (4-up) | 1024 vs 768 | Card height **283px @1024 → 256px @768** at similar widths (305 vs 342). Cosmetic reflow, no clipping. | `cards-1024.png`, `cards-768.png` | P3 |

### Forms — lead form (contacts.html)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| F1 | Input font-size triggers iOS Safari focus-zoom on mobile | `.pfg-form input` / `.form-control` | 390, 360 | Measured **font-size 15px on inputs at every viewport incl. mobile**. iOS Safari auto-zooms when a focused input's font-size is **< 16px**, jolting the layout. Bump mobile input font-size to ≥16px (visual-only). | `form-390.png`, `form-360.png` | P1 |
| F2 | Consent checkbox + its label hit area are below the 44px tap floor | `.pfg-consent input[type=checkbox]` + wrapping `<label>` | 390, 360 | Checkbox box **18×18 px**; wrapping `label.pfg-consent` hit area **330×36 px** — **36px tall < 44px** (WCAG 2.5.5). The label widens the target horizontally but height stays under floor. | `form-390.png` | P1 |
| F3 | Submit and field heights are healthy | submit button, text inputs, map | all | Submit **261×64**, inputs **55px tall**, map iframe **420px** fixed down to 300px width — all good. Positive finding. | `form-1440.png` | — |

### Footer (shared chrome — all 11 pages)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| FT1 | Footer menu links measure **26px tall** — under the 44px tap floor, and contradicting the documented 44px hit-zone | `.site-footer a` (footer nav group) | 390, 360 (all) | DOM-measured: footer menu links **57×26 / 82×26 / 46×26 / 65×26 px** (15 visible links). `CLAUDE.md`/`custom.css:565-571` claims a 44px footer hit-zone — **the live render does not apply it to these links** (DOM-vs-CSS discrepancy, RESEARCH Pitfall 5). Reconcile in the relevant later phase: either the rule's selector misses this link group or it is overridden. | `footer-390.png`, `footer-360.png` | P1 |
| FT2 | Gold top-border present and correct | `.site-footer` border-top | all | Measured **`3px solid rgb(236,171,35)`** (= `#ecab23` gold) at every viewport — matches the contract's footer signature (UI-SPEC accent list). Positive finding. | `footer-1440.png` | — |
| FT3 | Footer is very tall when columns stack on mobile | `.site-footer` | 390, 360 | Footer box **1732px @390 / 1755px @360** (vs 1067px @1440). Expected from stacked columns; flagged as low-priority vertical-density review, not a defect. | `footer-360.png` | P3 |

### Title-bar (10 inner pages; absent on index.html)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| T1 | Fixed **550px** title-bar wastes ~half the viewport for a one-line page heading on tablet/landscape | `.pbmit-title-bar-wrapper` | 1440, 1024, 768 | Measured **min-height 550px** at 1440/1024/**768**; only collapses to **214px at ≤390**. A 550px band on a 768-wide tablet to show "Услуги" alone is disproportionate vertical real estate. Consider a smaller min-height tier between 768 and 390. | `titlebar-768.png`, `titlebar-1024.png` | P2 |
| T2 | Title-bar H1 line-height is tight but single-line-safe | `.pbmit-title-bar-wrapper h1` | 1440–768 | Measured **font-size 70px, line-height 70px** (lh == fs). Fine for the current one-word/short titles; would clip on a wrapped two-line title — note for type-scale work. Mobile **32px / 50px** is comfortable. | `titlebar-1440.png` | P3 |

### Imagery (index.html — 12 `<img>`; backgrounds vendor-owned, RESEARCH Q2)

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| I1 | `about-01.jpg` is rendered far below its natural resolution (oversized asset) | `index.html` `<img about-01.jpg>` | all | Natural **900×1000**, rendered **273×304 (1440) … 330×367 (390)** — serving a 900px asset into a ~300px box. Aspect ratio is preserved (no distortion); this is a **payload/IMG-01** note. Bulk WebP/AVIF re-encode is **v2/PERF-01 (out of scope)** — record only. | `hero-1440.png` (context) | P3 |
| I2 | `about-02.png` / `infobox-img.png` render at sensible sizes | `index.html` imagery | all | `about-02.png` natural 381×680 ≈ render 363–381 wide (1:1-ish); `infobox-img.png` 120×40 exact. No distortion. Positive finding. | — | — |

### Global / typography / layout

| # | What | Where | Viewport(s) | Why (DOM evidence) | Screenshot | Sev |
|---|------|-------|-------------|--------------------|------------|-----|
| G1 | **No horizontal overflow anywhere** — responsive layout is sound at the document level | `documentElement` | 1440, 1024, 768, 390, 360 | Measured `scrollWidth == clientWidth` (**overflow = 0px**) on both `about.html` and `index.html` at **all five viewports**. No broken wrapping / runaway element. Strong positive baseline finding. | all `*-360.png` | — |
| G2 | Headline line-height policy is inconsistent across blocks | hero (HE1) vs title-bar (T2) | 1440 | Desktop hero lh < fs (170/150) while title-bar lh == fs (70/70); the contract's `clamp()` type scale + ratio 1.25 (TOK-03) should normalize heading line-heights so none sits below 1.0. | `hero-1440.png`, `titlebar-1440.png` | P2 |

### Accepted documented exceptions (not new findings)

- **Mobile header search target-size (H2)** — theme-owned, carried as an accepted exception per MEMORY `ui-audit-2026-06-23` and RESEARCH Open Question 2. This run measured the control at **44×44 px**, so it did **not** surface as a hard blocker; it maps to **WCAG 2.2 SC 2.5.8**, which is outside the `wcag2a/2aa/21a/21aa` axe tag set scanned in AUD-01. Logged as a standing exception, **not** scheduled work.

### Absent features (net-new-or-descope — NOT findings of existing UI)

These are confirmed **absent on every page** (RESEARCH Q3 + Anti-Pattern); they are recorded so later phases treat them as net-new or descope, never as "polish existing UI":

| Feature | Requirement | Status | Disposition |
|---------|-------------|--------|-------------|
| Pricing / tariff block | CNV-02 | **Absent** — zero `pricing`/`тариф`/`price-table` markup on any of 11 pages | Net-new in a later phase, or descope. Not auditable today. |
| FAQ accordion | CMP-05 | **Absent** — no `.accordion` markup; theme handler exists in `js/scripts.js:309` but no page instantiates it | Net-new or descope. The single "популярный" pricing-tier highlight in UI-SPEC depends on CNV-02 existing first. |
| Live modal / lightbox | CMP-06 | **Absent** — Magnific Popup loaded on all 11 pages but triggers `.pbmin-lightbox-video` / `a.pbmit-lightbox` appear in **zero** markup | Descope; UI-SPEC already gates modal rules to "only if actually instantiated" — confirmed not instantiated. |

These three are flagged here only to keep them out of the existing-UI problem list; their scoping is reconciled against the contract in plan **01-04**.
