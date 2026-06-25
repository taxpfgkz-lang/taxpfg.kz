# 01-CONFLICT-CATALOG — `custom.css` ↔ vendor conflict surface (AUD-03)

- **Milestone:** v1.0 — Production UI Polish
- **Phase:** 01 — baseline-audit-ui-design-contract
- **Plan:** 01-02 (AUD-03)
- **Date:** 2026-06-25
- **Source of truth:** `css/custom.css` (read live), `css/base.css`, `js/scripts.js`, `js/custom.js`, all 11 `*.html`

## Purpose

This catalog freezes the override-accounting and the hard do-not-touch boundary so Phases 2–5 can refactor the premium layer without breaking theme JS/animation hooks.

The **`!important` budget is the Phase 2 net-new ≈ 0 floor**: Phase 2 may relocate or consolidate existing overrides but must not *grow* the project's `!important` count. The verified baseline is **59** (the AUD-03 / ROADMAP figure = `grep -c '!important' css/custom.css`). See the reconciliation note below for the functional-vs-comment breakdown.

**Scope boundary:** the 59 figure is **`custom.css`-only** — the project's own override budget. Vendor `!important`s (in `style.css`, `responsive.css`, `shortcode.css`, `base.css`) are context, NOT part of this budget (RESEARCH Pitfall 2). Do not fold vendor counts into the floor.

---

## Count reconciliation (verified live)

| Measure | Command | Result |
|---|---|---|
| Lines containing `!important` | `grep -c '!important' css/custom.css` | **59** — matches AUD-03 / ROADMAP baseline exactly |
| Raw `!important` tokens | `grep -o '!important' css/custom.css \| wc -l` | 61 |
| Comment-prose lines (non-functional) | lines 317, 643, 644 | 3 lines / 4 tokens |
| **Functional declaration tokens** | 61 − 4 | **57** |
| **Functional declaration lines** | 59 − 3 | **56** |

**Delta note (not a discrepancy — a clarification):** the documented baseline **59 matches `grep -c` exactly**, so the AUD-03 number is correct as a line count. The nuance: 3 of those 59 lines are Russian explanatory comments that contain the literal word `!important` (line 317 inside the reduced-motion history note ×2 tokens; lines 643–644 inside the Stage-13 banner ×1 token each), so they are NOT live CSS declarations. The true **functional override budget is 57 declarations across 56 lines**. One declaration line carries two tokens (line 191: `bottom` + `right`), which is why functional tokens (57) exceed functional lines (56).

**Budget guidance for Phase 2:** treat **57 functional `!important` declarations** as the net-new ≈ 0 ceiling. The "59" headline number stays valid for grep-based audits, but anyone diffing actual rules should target 57.

---

## !important ledger

Every functional `!important` in `css/custom.css`, with the vendor rule it beats. "Vendor target" cites the beaten rule when the adjacent Russian comment names it (`file:line`); otherwise marked **uncited** (Phase 2 must confirm the real vendor selector before touching). Comment-prose occurrences (lines 317, 643, 644) are excluded — they are not declarations.

| # | custom.css line | selector | property | vendor rule it beats |
|---|---|---|---|---|
| 1 | 182 | `@max-575 .pbmit-slider-one .pbmit-slider-title` | `font-size` | `shortcode.css` slider-title font-size (file cited §10.2, line uncited) |
| 2 | 183 | `@max-575 .pbmit-slider-one .pbmit-slider-title` | `line-height` | `shortcode.css` slider-title (line uncited) |
| 3 | 191 | `.pbmit-backtotop.active` | `bottom` | `base.css` `.pbmit-backtotop` (cited §8.2, line uncited) |
| 4 | 191 | `.pbmit-backtotop.active` | `right` | `base.css` `.pbmit-backtotop` (line uncited) |
| 5 | 192 | `.pbmit-backtotop:hover` | `bottom` | `base.css` `.pbmit-backtotop` (line uncited) |
| 6 | 202 | `@max-1200 .pbmit-menu-wrap, .active .pbmit-menu-wrap, .pbmit-mobile-menu-bg, .active .pbmit-mobile-menu-bg` | `transition-duration` | theme off-canvas open anim ~1500ms — **uncited** |
| 7 | 203 | `@max-1200` (same group) | `transition-delay` | theme off-canvas open anim — **uncited** |
| 8 | 341 | `@prefers-reduced-motion` premium micro-interactions group | `transition` | premium-layer's own transitions + theme micro-interactions — **uncited** (self-override, scoped killer) |
| 9 | 342 | `@prefers-reduced-motion` (same group) | `transform` | premium-layer's own transforms — **uncited** (self-override) |
| 10 | 344 | `@prefers-reduced-motion html` | `scroll-behavior` | global smooth-scroll — **uncited** (self-override) |
| 11 | 392 | `@min-1201 .pbmit-header-style-1 .pbmit-header-content` | `border-color` | theme header border `#7c898d` (`base.css`/`style.css`) — **uncited** |
| 12 | 555 | `@min-1201 .pbmit-slider-one .pbmit-slider-title` | `letter-spacing` | `shortcode.css` `letter-spacing:-5.1px` (file cited §10.2, line uncited) |
| 13 | 655 | `.section-xlt, .pbmit-bg-color-light.section-xlt` | `padding-top` | `responsive.css:145` (cited) |
| 14 | 656 | `.section-xlt, .pbmit-bg-color-light.section-xlt` | `padding-bottom` | `responsive.css:145` (cited) |
| 15 | 661 | `@max-768 .section-xlt …` | `padding-top` | `responsive.css:145` (cited) |
| 16 | 662 | `@max-768 .section-xlt …` | `padding-bottom` | `responsive.css:145` (cited) |
| 17 | 668 | `@max-480 .section-xlt …` | `padding-top` | `responsive.css:145` (cited) |
| 18 | 669 | `@max-480 .section-xlt …` | `padding-bottom` | `responsive.css:145` (cited) |
| 19 | 678 | `.why-choose-us-section-one` | `padding-top` | `responsive.css:234` (cited) |
| 20 | 679 | `.why-choose-us-section-one` | `padding-bottom` | `responsive.css:234` (cited) |
| 21 | 683 | `@max-768 .why-choose-us-section-one` | `padding-top` | `responsive.css:234` (cited) |
| 22 | 684 | `@max-768 .why-choose-us-section-one` | `padding-bottom` | `responsive.css:234` (cited) |
| 23 | 689 | `@max-480 .why-choose-us-section-one` | `padding-top` | `responsive.css:234` (cited) |
| 24 | 690 | `@max-480 .why-choose-us-section-one` | `padding-bottom` | `responsive.css:234` (cited) |
| 25 | 700 | `.our-process-section-one` | `padding-top` | `responsive.css:310` (cited) |
| 26 | 701 | `.our-process-section-one` | `padding-bottom` | `responsive.css:310` (cited) |
| 27 | 705 | `@max-768 .our-process-section-one` | `padding-top` | `responsive.css:310` (cited) |
| 28 | 706 | `@max-768 .our-process-section-one` | `padding-bottom` | `responsive.css:310` (cited) |
| 29 | 711 | `@max-480 .our-process-section-one` | `padding-top` | `responsive.css:310` (cited) |
| 30 | 712 | `@max-480 .our-process-section-one` | `padding-bottom` | `responsive.css:310` (cited) |
| 31 | 720 | `.ihbox-section-one` | `padding-top` | theme section padding (DOM-measured 37/32) — **uncited** |
| 32 | 721 | `.ihbox-section-one` | `padding-bottom` | theme section padding — **uncited** |
| 33 | 725 | `@max-768 .ihbox-section-one` | `padding-top` | theme section padding — **uncited** |
| 34 | 726 | `@max-768 .ihbox-section-one` | `padding-bottom` | theme section padding — **uncited** |
| 35 | 731 | `@max-480 .ihbox-section-one` | `padding-top` | theme section padding — **uncited** |
| 36 | 732 | `@max-480 .ihbox-section-one` | `padding-bottom` | theme section padding — **uncited** |
| 37 | 743 | `.about-section-one` | `padding-top` | `base.css:528` `.section-xlt` area (cited §13.5) |
| 38 | 744 | `.about-section-one` | `padding-bottom` | `base.css:528` area (cited) |
| 39 | 748 | `@max-768 .about-section-one` | `padding-top` | `base.css:528` area (cited) |
| 40 | 749 | `@max-768 .about-section-one` | `padding-bottom` | `base.css:528` area (cited) |
| 41 | 754 | `@max-480 .about-section-one` | `padding-top` | `base.css:528` area (cited) |
| 42 | 755 | `@max-480 .about-section-one` | `padding-bottom` | `base.css:528` area (cited) |
| 43 | 765 | `.pbmit-bg-color-secondary, .pbmit-bg-color-blackish` | `padding-top` | theme dark-section padding — **uncited** |
| 44 | 766 | `.pbmit-bg-color-secondary, .pbmit-bg-color-blackish` | `padding-bottom` | theme dark-section padding — **uncited** |
| 45 | 771 | `@max-768` (same dark group) | `padding-top` | theme dark-section padding — **uncited** |
| 46 | 772 | `@max-768` (same dark group) | `padding-bottom` | theme dark-section padding — **uncited** |
| 47 | 778 | `@max-480` (same dark group) | `padding-top` | theme dark-section padding — **uncited** |
| 48 | 779 | `@max-480` (same dark group) | `padding-bottom` | theme dark-section padding — **uncited** |
| 49 | 809 | `.pbmit-service-box` | `padding` | theme service-box padding — **uncited** |
| 50 | 853 | `.marquee-section, .pbmit-marquee-effect-style-1` | `background-color` | theme golden marquee background — **uncited** |
| 51 | 858 | `.pbmit-marquee-effect-style-1 .pbmit-tag-wrapper h2, h2.pbmit-element-title` | `color` | theme marquee text color — **uncited** |
| 52 | 920 | `@max-575 .pbmit-title-bar-wrapper` | `background-image` | theme title-bar `background-image:url(...)` — **uncited** |
| 53 | 924 | `@max-575 .pbmit-title-bar-content` | `min-height` | theme title-bar min-height — **uncited** |
| 54 | 925 | `@max-575 .pbmit-title-bar-content` | `padding-top` | theme title-bar padding — **uncited** |
| 55 | 926 | `@max-575 .pbmit-title-bar-content` | `padding-bottom` | theme title-bar padding — **uncited** |
| 56 | 929 | `@max-575 .pbmit-tbar-title` | `font-size` | theme title font-size — **uncited** |
| 57 | 932 | `@max-575 .pbmit-breadcrumb` | `font-size` | theme breadcrumb font-size — **uncited** |

**Total: 57 functional `!important` declarations across 56 lines.** The AUD-03 baseline of **59** = `grep -c '!important' css/custom.css` (line count, which also catches the 3 comment-prose lines at 317/643/644). Both figures reconcile — see the Count reconciliation table. **No silent mismatch:** grep-c line count = 59 (= baseline ✓); functional declarations = 57.

**Citation summary:** 24 declarations cite an exact vendor `file:line` (the §13.1–13.3 `responsive.css` overrides and §13.5 `base.css:528`). 2 more cite the vendor *file* but not the line (`shortcode.css`, §8.1/§10.2). The remaining 31 are **uncited** — Phase 2 must confirm the actual beaten vendor selector before relocating or dropping them.

---

## Do-not-touch theme classes/attributes

> **Vendor read-only boundary:** every file below except `css/custom.css`, `css/base.css`, and `js/custom.js` is vendor/theme-owned and MUST NOT be edited (stated at `css/custom.css:1-4`, `js/custom.js:113-130`, and CLAUDE.md Constraints). The namespaces here are *targeted* by the custom layer for override but are NEVER renamed, removed, or re-owned. Renaming any of them in markup detaches the theme JS that binds to it.

| Namespace | What binds to it | Breakage if renamed/removed |
|---|---|---|
| `swiper-*` (`.swiper-slider`, `.swiper-wrapper`, `.swiper-slide`, `.swiper-pagination`, `.swiper-button-next/prev`) | `js/scripts.js` — `$(".swiper-slider")` enumeration and `new Swiper('.pbmit-element-viewtype-carousel-*', …)` init (scripts.js:32–177). The services marquee runs on the same Swiper instance. | Hero slider stops initializing; services **marquee dies**; and `js/custom.js` `initMarqueeSpeed` (which sets the 40000ms inline `transition-duration`) loses its target element and silently no-ops. |
| `data-aos*` (`data-aos`, `data-aos-delay`, `data-aos-duration`) | `js/scripts.js` — `AOS.init({…})` (scripts.js:245+) reads these attributes on scroll. | Animate-on-scroll reveals stop firing; content that starts at `opacity:0` may stay hidden. AOS reads attributes at init, so renaming the attribute = no animation + possible invisible content. |
| `pbmit-*` (all GudFin theme structural/visual classes: `.pbmit-header-style-1`, `.pbmit-slider-one`, `.pbmit-title-bar-wrapper`, `.pbmit-btn`, `.pbmit-menu-wrap`, `.pbmit-marquee-effect-style-1`, `.pbmit-backtotop`, `.pbmit-element-service-style-2`, etc.) | Theme CSS (`style.css`, `shortcode.css`, `responsive.css`, `base.css`) for layout/visual + theme JS hooks (sticky header, menu dropdowns, back-to-top, charts) in `scripts.js`/`gsap-animation.js`. The entire `!important` ledger above *targets* `pbmit-*`/theme classes. | Layout collapses (theme rules no longer match), JS hooks detach, and **every override in the ledger above stops applying** because its selector no longer matches. The custom layer owns none of these — it only overrides them by cascade. |

### Cross-referenced conflict-surface boundaries (UI-SPEC Hard Constraints)

- **Off-canvas-safe constraint:** do NOT apply `filter`, `backdrop-filter`, or `transform` to any ancestor of the mobile off-canvas menu (`.pbmit-menu-wrap`, which is `position:fixed; height:100%` inside `.pbmit-header-content` at ≤1200px). Doing so makes the ancestor a containing block for the fixed child → `height:100%` collapses to header height (~49px) and the menu breaks into a narrow white strip. This is why the §9.3 glass header is gated to `@min-width:1201px` (`css/custom.css:378-397`). Any new decorative effect using those three properties must be desktop-gated the same way.
- **Load-order constraint:** `custom.css` MUST remain the **last** stylesheet (`index.html:54`) and `custom.js` the **last** script (`index.html:1057`), or the cascade overrides stop winning and the post-init DOM patches run before theme JS. This ordering is load-bearing across all 11 pages.

---

## Unused vendor: chart.js

- **Status:** `js/chart.js` (Chart.js 4.5.0) is **vendored but referenced by zero pages** — `grep -ril "chart" --include="*.html"` returns nothing across all 11 HTML files (RESEARCH Q4, re-verified live 2026-06-25).
- **Live cost:** zero — it is never `<script>`-loaded by any page, so it contributes zero runtime bytes and zero parse cost. It is dead weight in the repo only.
- **Disposition:** removal is **OUT OF SCOPE for v1.0** — deferred to **v2 / PERF-02**. Recorded here so later phases do not "discover" the unreferenced file and act on it within this milestone. Leave `js/chart.js` in place.

---

## Verification (read-only confirmation)

- `git status` must show changes only under `.planning/` — no edits to `css/*`, `js/*`, or `*.html`. This plan performed static analysis (grep/read) only.
- `grep -c '!important' css/custom.css` → 59 (baseline confirmed).
- `grep -ril "chart" --include="*.html" .` → no matches (chart.js unused confirmed).
