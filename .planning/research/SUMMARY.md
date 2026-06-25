# Project Research Summary

**Project:** taxpfg.kz — Production UI Polish
**Domain:** Brownfield UI polish of a no-build, vendored-theme static marketing site (11 pages, GudFin/PBMIT theme + Bootstrap 5.2 + thin `pfg-*` override layer)
**Researched:** 2026-06-25
**Confidence:** HIGH

## Executive Summary

This is not a greenfield build — it is a disciplined visual hardening of a live, conversion-driven static site. The site already has the skeleton of a design system: a `--pfg-*` token block in `css/custom.css` (ink + gold, shadows, radii, easing) layered over the theme's `--pbmit-*` tokens. The milestone's job is to **consolidate, formalize, and enforce** that system across 11 hand-duplicated pages without a build step, without touching vendor files, and without changing one byte of behavior (forms→WhatsApp, analytics, routing, JSON-LD, brand animations). The runtime stack is fixed; the only editable surface is `css/custom.css`, `css/base.css`, and `js/custom.js` — and in practice `base.css` is theme-owned too, so the safe surface is really `custom.css` + `custom.js`.

The expert approach here is **tokens-first, bottom-up**: define a complete spacing/type/color/z-index token sheet on `:root`, then apply it to base elements, then to components, then to page-level conversion blocks — and only then run a dedicated a11y pass and cross-device verification. The spacing/type contract is the root dependency: cards, pricing tiers, and hero all inherit it, so it must land before any component polish or fixes will not compose. Fluid type via `clamp()` and `text-wrap: balance/pretty` deliver responsive typography with no media queries and no JS, which is the right no-build move for the "no ugly Russian wrapping" requirement.

The dominant risks are all regressions, not missing features. Three stand out: (1) the override layer already carries ~59 `!important` fighting the theme — reflexively adding more turns the cascade unreadable; the fix is **targeted specificity + design tokens + source order, never `@layer`** (see resolved conflict below); (2) shared header/footer/`<head>` are copy-pasted into all 11 pages with no include mechanism, so any chrome edit must be CSS-first or a verified "change-all-11" pass; (3) the a11y floor (visible focus, AA-contrast gold-as-text token, scoped `prefers-reduced-motion`) is encoded in rules that *look* like ordinary styling but are load-bearing — a polish edit silently erodes it. The single most important process rule: **capture the per-page Lighthouse/axe baseline BEFORE any edit** — it is the "не хуже" floor every later phase is measured against.

## Key Findings

### Recommended Stack

The stack is fixed (pure static HTML5/CSS3/vanilla-ES5-JS, no npm, no bundler, vendor libs read-only). STACK.md is therefore a *technique* selection under that constraint, and its conclusions are HIGH-confidence and verified against MDN (2026-06-25).

**Core techniques:**
- **Design tokens (CSS custom properties) on `:root`** — the backbone; values resolve independently of specificity, so they sidestep the override war entirely.
- **Targeted specificity (one extra class) + load-order guarantee** — how `custom.css` beats the theme cleanly; `custom.css`/`base.css` MUST stay last in every `<head>`.
- **`clamp()` fluid type + `text-wrap: balance/pretty`** — responsive typography and clean wrapping with zero media queries, zero JS, zero dependency.
- **`:where()` for the overridable baseline only** — specificity 0; never for rules that must beat the theme.
- **Audit tooling with no project install** — `python -m http.server`, `npx lighthouse` per page, `@axe-core/playwright` viewport sweep at Bootstrap breakpoints.

### The Resolved Conflict — `@layer` is OUT of scope

STACK.md (HIGH) and ARCHITECTURE.md (MEDIUM) disagreed on CSS cascade layers. **STACK.md is correct on the cascade mechanics, and this resolution is binding for the roadmap and design contract:**

- Per the CSS cascade (MDN, verified 2026-06-25), for normal declarations **unlayered styles always beat layered styles, regardless of specificity.** Bootstrap 5.2 and every GudFin theme file ship **unlayered**.
- Therefore wrapping `custom.css` in `@layer overrides` would make our overrides **LOSE** to the theme and force us to add *more* `!important` — the exact opposite of the goal.
- The only way `@layer` could help is loading vendor CSS into a layer via `@import … layer(vendor)`, which means re-routing vendor loading across 11 `<head>`s — a high-risk structural change for no gain.

**Decision: the override layer (`custom.css`/`base.css`) stays UNLAYERED and wins by source-order + targeted specificity (one-extra-class). `@layer` is FORBIDDEN for theme overrides and is OUT OF SCOPE for this milestone.** ARCHITECTURE.md's "pilot `@layer` for new `.pfg-*` components" suggestion is explicitly NOT adopted. The ~59 `!important` are reduced via specificity, design tokens, and source order — not cascade layers — and the target is a *measured reduction*, not zero (some are legitimately irreducible against theme media-query rules).

### Expected Features

FEATURES.md frames "feature" as a UX/CRO pattern, not a new app capability (logic is frozen). HIGH confidence on established CRO/UX heuristics; MEDIUM on KZ-specific conversion nuance.

**Must have (table stakes — P1, the production floor):**
- Hero value-prop clarity + single primary CTA + readable contrast over the slider
- Lead form: visible labels, minimal fields, inline validation, distinct success/error with `aria-live`, mobile input types
- FAQ accordion with correct ARIA APG semantics + keyboard operability (a11y-floor)
- Service-grid card consistency (equal height, aligned CTAs)
- Above-the-fold trust row; credible footer parity across all 11 pages
- Spacing/type-scale contract applied site-wide; focus + AA contrast at/above baseline

**Should have (differentiators — P2, after table stakes):**
- Transparent 3-tier pricing with exactly one "популярный" highlight + per-tier CTA
- Sticky mobile CTA bar (must resolve the WhatsApp-float collision)
- Specific attributed testimonials / credential-badge strip; guarantee / risk-reversal copy near CTAs

**Defer (v2+, out of this milestone):**
- Payload/image optimization (WebP/AVIF), templating to kill ×11 duplication, any backend/CRM — all separate milestones.

**Anti-features to forbid in the contract:** entry/exit pop-ups, fake urgency timers, stock-photo testimonials, auto-rotating multi-message hero, placeholder-only labels, long lead forms, generic CTA copy, color-only state feedback, highlighting every pricing tier.

### Architecture Approach

ARCHITECTURE.md (HIGH overall) confirms the system already lives centrally: all 11 pages link the *same* `custom.css`, so **a single CSS rule reliably reaches every page** — visual consistency is solved centrally, and the token layer is the de-facto "include" for look. The risk is purely **markup/content drift** (a nav link, phone number, stale class), which CSS cannot fix.

**Major components / decisions:**
1. **Token sheet** — the canonical `:root` block at the top of `custom.css`; grow it, do not scatter. Two tiers (primitive + semantic). Breakpoints are a documented convention constant, not a token (`var()` cannot be used in `@media`).
2. **Component inventory** — buttons, inputs/forms, cards, nav (desktop + off-canvas), header/sticky, hero/slider, marquee, pricing, FAQ/accordion, info-box, footer, eyebrow, floating WhatsApp, breadcrumb, modal. Each specified as: owned selector, vendor selector overridden, token deps, states, responsive notes.
3. **11-page consistency strategy** — CSS-first (zero-risk) for everything visual; an optional dev-time Node drift-audit script (a lint, not a build, ships nothing) to catch markup drift; **header JS-injection is rejected** (theme JS binds the header at `DOMContentLoaded`); footer injection is last-resort only.
4. **JS safety** — `custom.js` stays last, vanilla, IIFE, idempotent, early-return-if-absent; never re-init/destroy theme widgets; never call Swiper `autoplay.stop()/start()` on the marquee; never touch the WhatsApp flow.

### Critical Pitfalls

1. **`!important` escalation war** — diagnose the winning vendor rule in DevTools and beat it with specificity; treat net-new `!important` as a budget near zero; each new one cites the vendor file:line it beats.
2. **Breaking theme JS by touching its hooks** — `swiper-*`, `aos-*`, `pbmit-*`, `data-*` look like style hooks but are JS hooks. Style by *adding* `.pfg-*` classes, never rename/remove/re-nest. No `filter`/`transform`/`backdrop-filter` on ancestors of the off-canvas menu (collapses it).
3. **Visual drift from editing 1 of 11 pages** — prefer CSS for shared chrome; when markup is unavoidable, change-all-11 in one atomic commit + grep-returns-11 + multi-page screenshot diff.
4. **A11y regressions** — never `outline:none` bare (use `:focus-visible`); gold text uses `--pfg-gold-ink` (>=5.4:1), never the `#ecab23` fill (~1.9:1) on white; new motion goes *inside* the scoped `prefers-reduced-motion` block; keep one `<h1>`, 44px targets, ARIA intact.
5. **Responsive breakage** — no fixed px content widths or `white-space:nowrap`; use `clamp()`/`max-width`/`%`; DOM-measure no-horizontal-scroll and >=44px targets at 1440/1024/768/390/360.
6. **The sticky-mobile-CTA vs WhatsApp-float collision** — both anchor bottom on mobile; must be deliberately reconciled (fold WhatsApp into the bar, or offset/hide one when the other is in view), never shipped overlapping.

## Recommended Build Order

Strict bottom-up; each implementation stage rests on the prior and ends with Playwright cross-device + a11y verification (the only QA available — there are no automated tests).

baseline audit -> tokens/spacing+type scale -> primitives -> components -> page conversion blocks -> a11y pass -> cross-device verification.

**The spacing/type contract is the root dependency everything downstream inherits** — it must land before any component polish or fixes will not compose. Components cannot be styled before tokens exist; page composites cannot be tuned before components are stable; a11y/contrast audits need final colors and markup; cross-device verification validates the integrated result last.

## Implications for Roadmap

Target **COARSE granularity, ~5–6 phases**.

### Suggested phases

**Phase 1 — Baseline Audit + UI Design Contract**
*Rationale:* Audit-first is a hard customer constraint; the baseline is the floor every later phase is measured against. *Delivers:* per-page Lighthouse/axe numbers, `!important` ledger, theme-JS do-not-touch list, and the contract encoding all hard constraints below. *This is a one-time phase, not a per-phase gate.* **Research flag: NO** (well-understood, codebase-grounded) — but it *produces* the data later phases depend on.

**Phase 2 — Token Sheet + Primitives (spacing/type/color foundation)**
*Rationale:* root dependency; components cannot be styled before tokens exist. *Delivers:* complete `:root` token sheet, fluid type, base element styling, focus ring, section rhythm. *Avoids:* pitfall 1 (tokens replace `!important`), pitfall 7 (Cyrillic transform). **Research flag: NO** (standard token/`clamp()` patterns).

**Phase 3 — Components**
*Rationale:* highest reuse, conversion-critical; depends on tokens. *Delivers:* buttons, forms, cards, nav, header, footer, hero, FAQ, WhatsApp float per the inventory with all states. *Avoids:* pitfalls 2 (theme-JS hooks), 4 (a11y states). **Research flag: YES** — exact per-page component coverage (which pages have pricing/FAQ/modal) must be enumerated by walking each page; confirm Magnific Popup is actually instantiated before writing modal rules.

**Phase 4 — Conversion Blocks + Differentiators**
*Rationale:* composites depend on stable components. *Delivers:* hero, transparent pricing tiers (one highlight + per-tier CTA), sticky mobile CTA bar, testimonials/badges, contacts form presentation. *Avoids:* pitfall 6 (sticky-CTA vs WhatsApp-float collision — explicit DoD item). **Research flag: YES** — the sticky-CTA/WhatsApp reconciliation and pricing-tier layout need a small design spike.

**Phase 5 — Accessibility Pass + Cross-Device Verification**
*Rationale:* contrast/focus audits need final colors and markup; verification validates the integrated result. *Delivers:* axe/Lighthouse >= baseline on all 11 pages, drift-audit pass, screenshot set, local-check command list. **Research flag: NO** (checklist-driven).

### Per-phase definition-of-done (must include in every implementation phase)

- Multi-breakpoint, **DOM-measured** Playwright check at **1440 / 1024 / 768 / 390 / 360** — `scrollWidth` <= viewport (no horizontal scroll), `getBoundingClientRect()` >= 44px on interactive elements, headings not clipped.
- **axe / Lighthouse = 0 new violations** vs. the Phase-1 baseline; any flag must match a documented accepted exception (mobile header search target-size).
- **JS smoke test** by hand: mobile menu open/close/Escape/backdrop, WhatsApp float + number, `.pfg-form`->`wa.me` message + status line, marquee, slider, reduced-motion (brand motion on / micro-interactions off).
- **change-all-11 grep** (returns 11) + multi-page screenshot diff for any shared-chrome edit.
- **Behavior-diff guard:** `wa.me` message, `WA_NUMBER`, analytics, routing, JSON-LD byte-identical.
- **`!important` budget:** net-new ~= 0; each cites the vendor rule it beats.

### Per-phase gates vs. one-time phases

- **One-time phase:** baseline capture + design contract (Phase 1). The drift-audit script is buildable anytime but exercised in the verification phase.
- **Per-phase recurring gates (NOT phases):** a11y floor, responsive DOM checks, `!important` budget, theme-JS smoke test, scope-creep behavior-diff, change-all-11. These are definition-of-done items repeated in every implementation phase.

### Research Flags

- **Needs research:** Phase 3 (per-page component coverage — pricing/FAQ/modal enumeration; Magnific Popup instantiation check), Phase 4 (sticky-CTA vs WhatsApp-float reconciliation + pricing-tier layout spike).
- **Standard patterns (skip research):** Phase 1 (audit/contract), Phase 2 (tokens/`clamp()`), Phase 5 (checklist verification).

## Hard Constraints (Design Contract Seeds)

Non-negotiable rules the UI design contract MUST encode:

- **`!important` budget:** do not exceed the current ~59; reduce where a touched rule can win by specificity/token instead. Each remaining/new one cites the vendor file:line it beats.
- **Visible focus always:** never a bare `:focus { outline:none }`; every interactive element keeps a visible `:focus-visible` indicator.
- **Contrast-verified text tokens only:** gold *text* uses `--pfg-gold-ink`; the `#ecab23` gold fill is for backgrounds/borders only, never small text on white. Re-measure contrast on any text color/background change.
- **Scoped motion only:** new decorative motion goes *inside* the existing `prefers-reduced-motion` block; brand motion (Swiper/marquee/GSAP) stays out of it; never reintroduce a universal motion killer.
- **Visual-only:** no copy/content rewrites, no form-flow/WhatsApp-message changes, no analytics/routing/JSON-LD edits. Off-scope findings get filed as backlog items, not fixed inline.
- **Vendor files read-only:** edits only in `css/custom.css`, `css/base.css`, `js/custom.js`.
- **No `@layer` for overrides** (resolved conflict above) — unlayered source-order + specificity only.
- **No build system:** no bundler/npm in the shipped site; `npx`/python audit tools are fine (not shipped).
- **Load order invariant:** `custom.css`/`base.css` last among CSS, `custom.js` last among JS, on all 11 pages.
- **One `<h1>` per page; 44px tap targets on mobile; `text-transform:none` on new Russian text elements.**

## Open Questions

Deferred unknowns to resolve during planning/execution (do not block the roadmap):

- **Per-page Lighthouse/axe baseline numbers** — unknown until the Phase-1 baseline run; they define the "не хуже" floor. Capture first.
- **`<img>` vs CSS-background asset inventory** — must be inventoried before choosing `<picture>` vs `image-set()` per asset (image work itself is a future milestone, but the inventory informs CLS guards).
- **Exact `<head>` font-loading config** — confirm current `font-display:swap` state and the real preload set against the live `<head>` + a Lighthouse run before changing anything (STACK/PITFALLS flagged MEDIUM here).
- **Whether unused `chart.js` (208 KB) deletion enters scope** — currently OUT (vendor read-only; payload milestone owns it); confirm it stays out.
- **Which pages actually have pricing / FAQ / modal** — enumerate by walking each page during the component phase; confirm Magnific Popup is instantiated before writing modal rules.
- **Final `!important` count after refactor** — target a measured reduction, not zero; some are irreducible against theme media-query rules.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack (techniques) | HIGH | Verified against MDN 2026-06-25 (`@layer`, `:where()` precedence); runtime constraints are fixed and explicit. Web search available this session. |
| Features | HIGH (general) / MEDIUM (KZ-specific) | Grounded in Baymard, W3C ARIA APG, Unbounce; KZ/RU SMB conversion nuance is reasoned, not study-backed. Web search available. |
| Architecture | HIGH | Empirically grounded in measured header/footer hashes and the documented `--pfg-*`/`--pbmit-*` token layers; the one MEDIUM (`@layer` pilot) is explicitly overruled by STACK. |
| Pitfalls | HIGH | Directly grounded in this repo's `CONCERNS.md`/`CONVENTIONS.md`/`TESTING.md` with file:line refs + established WCAG/CSS behavior. Note: PITFALLS ran with **no web search** (training knowledge only); font/preload specifics flagged MEDIUM. |

**Overall confidence:** HIGH

### Gaps to Address

- Capture per-page Lighthouse/axe baselines as the first action of Phase 1 — they are the regression floor.
- Confirm live `<head>` font-loading config before any typography phase (the one MEDIUM-confidence area shared by STACK and PITFALLS).
- Enumerate per-page component coverage during the component phase rather than assuming.

## Sources

Research was **codebase-grounded** — the primary sources throughout are the project's own maps (`.planning/PROJECT.md`, `.planning/codebase/CONCERNS.md`, `CONVENTIONS.md`, `TESTING.md`, `STRUCTURE.md`, `ARCHITECTURE.md`) plus project memory (`ui-audit-2026-06-23.md`, `workflow-api-proxy-balance.md`). Web access was **partial across researchers**: STACK and FEATURES had web access (STACK verified `@layer`/`:where()` against MDN 2026-06-25; FEATURES cited Baymard, W3C ARIA APG, Unbounce). PITFALLS had **no web access** and rests on the codebase map + established CSS/WCAG/web-font behavior; its font/preload MEDIUM-confidence items should be confirmed against the live `<head>` + a Lighthouse run during the audit phase.

### Primary (HIGH confidence)
- `.planning/codebase/` map files — `!important` count, 11-page duplication, token layers, theme-JS hooks, off-canvas filter trap, no-test QA model (all with file:line refs)
- MDN — CSS `@layer` precedence + `:where()` specificity (verified 2026-06-25)
- Baymard Institute (form field count/labels/validation), W3C ARIA APG (accordion pattern)

### Secondary (MEDIUM confidence)
- Unbounce landing-page CRO heuristics
- KZ/RU SMB conversion nuance (reasoned from general principles)

### Tertiary (LOW confidence / needs validation)
- Exact current `<head>` font-loading config and per-page Lighthouse/axe baselines — unverified until the audit run

---
*Research completed: 2026-06-25*
*Ready for roadmap: yes*
