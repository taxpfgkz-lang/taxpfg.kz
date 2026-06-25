# Architecture / Design-System Research

**Domain:** Production UI polish of a brownfield no-build static site (vendored Bootstrap + GudFin theme + thin custom override layer)
**Researched:** 2026-06-25
**Overall confidence:** HIGH (grounded in the project's own codebase maps and the existing `--pfg-*` token layer; cascade reasoning is well-established CSS)

## Executive Summary

The site already has the bones of a design system: a `--pfg-*` token block at `css/custom.css:283-302` (ink + gold, shadows, radii, easing) sitting on top of the theme's `--pbmit-*` tokens in `css/base.css:21-49`. The job of this milestone is not to invent a system but to **consolidate, formalize, and make it enforceable** across 11 duplicated-markup pages without a build step and without touching vendor files.

The architecture has three immovable constraints that shape every recommendation: (1) **vendor/theme files are read-only** — only `css/custom.css`, `css/base.css`, and `js/custom.js` may change, and in practice `base.css` is theme-owned too, so the safe editing surface is really just `custom.css` + `custom.js`; (2) **no build** — no partials, no preprocessor, no minifier, so DRY-ing shared chrome must happen by discipline or by carefully-scoped runtime JS, not by a compile step; (3) **logic-safe** — Swiper, GSAP, AOS, the mobile menu, and the lead-form→WhatsApp flow must keep working, which forbids any change that reorders scripts, re-inits theme widgets, or mutates the markup those widgets bind to.

The single highest-leverage architectural move available without a build is **CSS cascade layers (`@layer`)**. Declaring an explicit layer order inside `custom.css` lets the override layer win the cascade by *position in the layer order* rather than by `!important` or specificity escalation — directly attacking the "59 `!important` + specificity wars" concern. Crucially this can be adopted incrementally and is safe: unlayered styles (everything the theme ships) always beat layered styles, so wrapping only *our* rules in a named layer would actually *lose* to the theme. The correct pattern is therefore to put the theme inside a low-priority layer via an `@import ... layer()` shim is impossible (we can't touch the `<link>` order cleanly), so the realistic play is a *scoped* layer block inside `custom.css` only for new work, while legacy `!important` overrides stay until migrated. This nuance is covered in the Token Layer and custom.css sections below.

The 11-page duplication problem is real and measured: hashing each page's `<header>`/`<footer>` shows **no two pages share an identical pair** — they drift by active-nav state, breadcrumb, and small hand-edits. Since all *visual* properties are driven from CSS that is already shared (one `custom.css` linked by all 11 pages), a single CSS change does reliably reach every page today. The risk is purely in **markup/content** drift (a nav link, a phone number, a stale class). The recommended strategy is a CSS-first contract plus a lightweight automated drift audit (a Node check script that is allowed to exist at the repo root because it is not shipped to the browser and does not constitute a "build"), with optional, carefully-bounded JS injection for footer-only content as a last resort.

## Token Layer

### Where tokens live — and why

| Concern | Decision | Rationale (load order) |
|---------|----------|------------------------|
| New/brand tokens (`--pfg-*`) | **`css/custom.css`** `:root` block (already at `:283-302`) | `custom.css` loads **last** (`index.html:30-54`), so its `:root` wins for any custom property name. This is the only file we own that is guaranteed to cascade over the theme. |
| Theme tokens (`--pbmit-*`) | **Leave in `css/base.css`** (read-only); reference via `var()`; override the *value* in `custom.css` `:root` only when a contrast/brand fix demands it | `base.css:21-49` is the theme's source of truth. Redefining a `--pbmit-*` name in `custom.css`'s `:root` overrides it globally because of load order — this is how `--pbmit-body-typography-color` is already darkened. Use sparingly and comment the override. |
| Do **not** create a third token file | Keep all custom tokens in `custom.css` | A new CSS file would need a new `<link>` in all 11 `<head>`s (11× edit, drift risk) and would have to be ordered after `custom.css`. Not worth it. `base.css` edits are off-limits per constraints even though it physically holds `:root`. |

**Verdict:** the token home is the existing `:root` block at the top of `custom.css`. Treat it as the canonical token sheet and grow it; do not scatter `var()` definitions through the file.

### Recommended token taxonomy

The existing block is good but partial. The contract should formalize a complete, two-tier set: **primitive** tokens (raw values) and **semantic** tokens (intent-named, referencing primitives). Two tiers is the right ceiling for a site this size — a third "component token" tier adds ceremony without payoff here.

```css
/* css/custom.css — extend the existing :root block at ~line 284 */
:root{
  /* ---- PRIMITIVES (raw scale values) ---- */
  /* Color — ink + gold brand (already present, keep hex identical to brand) */
  --pfg-ink:        #16222d;  --pfg-ink-deep: #0f1820;
  --pfg-gold:       #ecab23;  --pfg-gold-deep:#d6960f;  --pfg-gold-ink:#7a560a;
  --pfg-paper:      #ffffff;  --pfg-paper-warm:#f6f4ef;
  --pfg-hairline:   rgba(22,34,45,.10);  --pfg-hairline-2: rgba(22,34,45,.16);

  /* Spacing scale (modular, 4px base) — formalize what is ad-hoc today */
  --pfg-space-1: 4px;  --pfg-space-2: 8px;  --pfg-space-3: 12px;
  --pfg-space-4: 16px; --pfg-space-6: 24px; --pfg-space-8: 32px;
  --pfg-space-12:48px; --pfg-space-16:64px; --pfg-space-24:96px;

  /* Type scale (clamp() for fluid, no media queries needed) */
  --pfg-fs-xs:  .8125rem;  --pfg-fs-sm: .9375rem; --pfg-fs-base: 1rem;
  --pfg-fs-lg:  clamp(1.125rem,1.05rem + .4vw,1.25rem);
  --pfg-fs-h3:  clamp(1.375rem,1.2rem + .9vw,1.75rem);
  --pfg-fs-h2:  clamp(1.75rem, 1.4rem + 1.6vw, 2.5rem);
  --pfg-fs-h1:  clamp(2.25rem, 1.7rem + 2.6vw, 3.25rem);
  --pfg-lh-tight:1.2; --pfg-lh-snug:1.35; --pfg-lh-body:1.6;

  /* Radii / shadows / motion (already present — keep) */
  --pfg-radius:14px; --pfg-radius-sm:10px; --pfg-radius-pill:999px;
  --pfg-shadow-sm: …; --pfg-shadow-md: …; --pfg-shadow-btn: …; --pfg-shadow-btn-h: …;
  --pfg-ease: cubic-bezier(.22,.61,.36,1);
  --pfg-tf-fast:.25s var(--pfg-ease); --pfg-tf:.4s var(--pfg-ease);

  /* z-index ladder (name the layers; theme uses arbitrary values) */
  --pfg-z-header: 1000; --pfg-z-dropdown: 1010; --pfg-z-offcanvas: 1040;
  --pfg-z-float: 1050;  --pfg-z-modal: 1060;

  /* ---- SEMANTIC (intent → primitive) ---- */
  --pfg-color-text:        #2a3640;  /* darker than theme #7c898d for AA */
  --pfg-color-heading:     var(--pfg-ink);
  --pfg-color-accent:      var(--pfg-gold);
  --pfg-color-link:        var(--pfg-ink);
  --pfg-color-link-hover:  var(--pfg-gold-deep);
  --pfg-surface:           var(--pfg-paper);
  --pfg-surface-alt:       var(--pfg-paper-warm);
  --pfg-section-y:         var(--pfg-space-24);  /* vertical section rhythm */
}
```

**Breakpoints are a special case.** CSS custom properties **cannot be used inside `@media` queries** (a media condition can't read `var()`). So the breakpoint "token" must be documented as a *convention constant* (match the theme's `--pbmit-responsive-breakpoint: 1200px` and Bootstrap's 576/768/992/1200/1400) and written as literal values in `@media` rules, with a comment pointing back to the token table. Do not try to engineer around this; it is a known CSS limitation.

**Fluid type via `clamp()` is the no-build win for the type scale** — it removes the need to redefine font sizes at each breakpoint in `responsive.css` (which we can't edit anyway), letting one `var(--pfg-fs-h1)` scale smoothly desktop→mobile.

### Cascade strategy — beating the theme cleanly

Three tools, in order of preference:

1. **Reference theme tokens, don't fight them.** Where the theme already reads `var(--pbmit-global-color)`, override the *token value* in `custom.css` `:root` and the change propagates everywhere the theme uses it — zero specificity battle. Best tool when a value is genuinely global (brand color, body text color).
2. **CSS cascade layers (`@layer`) for new component styles.** Inside `custom.css`, declare `@layer pfg-base, pfg-components, pfg-overrides;` and author new `.pfg-*` work in those layers. Because *unlayered* rules always outrank *layered* ones, keep theme-overriding rules **unlayered** (or in a layer declared after an empty placeholder for the theme — but since we can't layer the theme's own files without touching their `<link>`s, the pragmatic rule is: **legacy theme-overrides stay unlayered/`!important`; brand-new self-contained `.pfg-*` components go in layers** so they're insulated from each other and easy to reason about). This is an incremental, reversible adoption — `@layer` is supported in all evergreen browsers (Chrome/Edge/Firefox/Safari 99+, ~2022+) and degrades by simply being ignored in ancient browsers, which is acceptable for this audience.
3. **Specificity, then `!important` as last resort.** When overriding a deeply-nested theme selector, first try matching its specificity with a contextual parent selector (the established pattern, e.g. `.pfg-prose p a:not(.pbmit-btn)`). Reserve `!important` for theme rules in media queries that cannot otherwise be beaten, and **always comment the vendor file:line being overridden** (existing convention at `custom.css:651-652`). The goal for this milestone: **do not increase the `!important` count; reduce it where a layer or token override can replace it.**

## custom.css Organization

`custom.css` is ~951 lines with numbered, dated "ЭТАП" banner blocks — a chronological journal. That worked for incremental audits but makes the file hard to navigate by *topic*. Recommendation: **keep the journal for history, but introduce a topic-based table of contents and migrate toward component blocks**, without a disruptive rewrite (a full reorder risks changing source order, which changes the cascade for equal-specificity rules — a real regression vector).

### Target structure (top to bottom)

```
/* ============================================================
   custom.css — PrimeFinance premium override layer
   Loaded LAST. Vendor read-only. Do not reorder <link> tags.
   ------------------------------------------------------------
   TABLE OF CONTENTS
   00  Tokens (:root primitives + semantic)        [the token sheet]
   01  Layer declaration (@layer order)
   02  Base / element overrides (body, links, headings, focus)
   03  Layout primitives (.pfg-section, .pfg-grid, container rhythm)
   04  Components
       04.1 Buttons (.pbmit-btn overrides + .pfg-cta-actions)
       04.2 Cards (.pfg-card)
       04.3 Forms & inputs (.pfg-form, .form-control, .form-select)
       04.4 Navigation / header (glass header, gated ≥1201px)
       04.5 Footer
       04.6 Hero / slider overrides (.pbmit-slider-area)
       04.7 Pricing / tariff blocks
       04.8 FAQ / accordion (.pbmit-accordion)
       04.9 Eyebrow / ledger-stroke signature
   05  Utilities (.pfg-muted, .pfg-lead, .pfg-prose, .pfg-sr-only)
   06  Accessibility (focus, reduced-motion scope, tap targets)
   07  Page-specific exceptions (scoped to a body/page class)
   ------------------------------------------------------------
   HISTORY: prior "ЭТАП N" journal blocks retained inline,
   tagged with the section they belong to.
   ============================================================ */
```

### Conventions to lock into the contract

- **Naming:** keep the two-namespace rule — `pfg-*` for owned elements, `pbmit-*` only as override *targets*, never authored. Modifiers `--alt` (double-dash, BEM-ish), states `is-` prefix. This is already consistent; the contract just ratifies it.
- **Sectioning:** every component block opens with a one-line banner naming the component and listing the vendor selectors it overrides. Keep the dense Russian "why" comments — they cite contrast ratios and vendor file:line and are genuinely load-bearing for a future editor who can't open theme files.
- **`!important` ledger:** add a short comment tag `/* !imp: beats responsive.css:NNN */` at each `!important` so the count is auditable and removals are safe. A grep for `!imp:` then becomes the migration backlog.
- **One concern per block; no scattering.** New work appends a *component* section, not a new dated journal block, unless it's a true cross-cutting audit pass.

## 11-Page Consistency Strategy

### The measured problem

Hashing each page's normalized `<header>` and `<footer>`:

```
404.html      header b37c4efb  footer 03e3c8af
about.html    header af414f69  footer 799b0849
…             (all 11 differ)  privacy & 404 share a footer; services & privacy share a header
```

No two pages share an identical header+footer pair. Differences come from legitimate per-page state (active nav `current-menu-item`, breadcrumb text, page title) *and* from latent hand-edit drift that nothing currently catches.

### What is already safe vs. what is at risk

- **Visual consistency is already centralized.** All 11 pages link the *same* `custom.css`. A single CSS rule change (a button radius, a section padding token) reliably reaches all 11 pages with no per-page work. **This is the design system's biggest asset and the reason a CSS-token contract is the right primary tool.** The token layer is the de-facto "include" for *look*.
- **Markup/content consistency is NOT centralized and cannot be without a build or runtime JS.** A nav link, phone number, footer copyright, or a structural class added to the header must be edited in 11 files.

### Recommended strategy (concrete, risk-assessed)

1. **CSS-first for everything visual (primary, zero-risk).** Drive all spacing, color, type, radius, shadow, and state styling from the token layer + component blocks in `custom.css`. Because the markup classes (`site-header pbmit-header-style-1`, `site-footer pbmit-footer-style-1`) are identical across pages, one CSS rule styles all 11. No per-page CSS.

2. **Automated drift audit (recommended, low-risk).** Add a Node check script at repo root (e.g. `tools/check-chrome.js`). It is **not a build step and ships nothing to the browser** — it just reads the 11 HTML files, extracts and normalizes `<header>`/`<footer>`/`<head>` (stripping the known per-page deltas: active-menu class, breadcrumb, title/meta), hashes the remainder, and fails if they diverge. Run it manually before any chrome edit. This converts the "edit 11 places correctly" gamble into a verifiable check. This respects the no-build constraint (it's a lint, not a compiler) and the logic-safe constraint (read-only, never writes HTML).
   - *Risk:* none to runtime; only a dev-time helper. Worst case it's ignored.

3. **Runtime JS injection of shared chrome — NOT recommended for header, conditionally OK for footer-only static content (high-risk, last resort).**
   - **Header injection is a trap.** The header is bound by theme JS: the sticky-header GSAP init (`gsap-animation.js`), the mobile off-canvas menu (`scripts.js` + `custom.js initMobileMenu`), and the search a11y patch all `querySelector` the header markup **at `DOMContentLoaded`**. Injecting/replacing header DOM after those binds would break the menu and sticky behavior — a direct violation of *logic-safe*. Do not do this.
   - **Footer is lower-risk** (no theme JS binds critical behavior to it), so a tiny `js/custom.js` function could inject a shared footer fragment. **But** it would cause a flash of missing footer (FOUC), hurt SEO crawlers that don't run JS, and add a maintenance fragment file. **Verdict: only if footer drift becomes unmanageable, and even then prefer the audit script.** If pursued, the fragment must be inlined as a JS template string (no `fetch`, which fails on `file://` and adds a request) and injected synchronously, and it must early-return if a footer already exists (idempotent, matching the `custom.js` convention).

4. **"Change-all-11" checklist discipline (always).** Any header/footer/`<head>`/nav edit is a single atomic commit touching all 11 files, verified by the audit script (step 2). Document this as a hard rule (it already exists informally in `CONCERNS.md` and the anti-pattern list).

**Bottom line:** make the design system live in `custom.css` (visual = solved centrally), guard markup with a dev-time audit script (drift = caught), and treat JS chrome-injection as an explicitly-rejected option for the header and a last-resort for the footer.

## Component Inventory

The contract must specify each component as: **owned selector(s) → vendor selector(s) overridden → token dependencies → states → responsive notes**. Enumerate by walking the actual markup (Bootstrap classes + `pbmit-*` shortcodes + `pfg-*` utilities). Grep confirms these are present across pages.

| Component | Primary selectors | Vendor base | States to specify | Notes |
|-----------|-------------------|-------------|-------------------|-------|
| **Button (primary/secondary)** | `.pbmit-btn`, `.pfg-cta-actions` | theme btn | default / hover / focus-visible / active / disabled | gold fill stays `#ecab23`; text-on-gold darkened for AA; `text-transform:none` for Russian |
| **Card** | `.pfg-card`, `.pfg-card--alt` | — (owned) | default / hover-lift (reduced-motion off) / focus-within | lift via `--pfg-shadow-md`; in `prefers-reduced-motion` block |
| **Input / Select / Textarea** | `.form-control`, `.form-select`, `.pfg-form` | Bootstrap + theme | default / focus (gold ring) / invalid / disabled / placeholder | select-arrow SVG fix already at `custom.css:83-89`; consent checkbox |
| **Form status / live region** | `.pfg-form-status.is-error/.is-ok` | — | error / ok / empty | `role=status aria-live=polite`; do not change WhatsApp logic |
| **Navigation (desktop)** | `.site-navigation ul.navigation > li > a` | `pbmit-header-style-1` | default / hover (underline grow) / active/current / focus-visible | glass header gated `≥1201px` — backdrop-filter must NOT wrap off-canvas |
| **Navigation (mobile off-canvas)** | `#site-navigation.active`, `body.pfg-menu-open` | theme off-canvas | open / closed / focus-trap | bound by `initMobileMenu`; do not restructure DOM; known search target-size flag accepted |
| **Header / sticky** | `.site-header`, `#masthead` | `pbmit-header-style-1` | normal / stuck (GSAP) | sticky via `gsap-animation.js`; z-index token |
| **Hero / slider** | `.pbmit-slider-area`, `.pbmit-slider-one` | Swiper | per-slide enter anim | index-only; animations are brand identity — keep; visually-hidden `<h1>` |
| **Services marquee** | `.swiper-slider.marquee` | Swiper autoplay | running | speed via `swiper.params.speed` only — never `autoplay.stop()` |
| **Pricing / tariff** | tariff block + `.pfg-card` | theme price/`ihbox` | default / featured / hover | verify per page; align CTA buttons |
| **FAQ / accordion** | `.pbmit-accordion` | theme accordion | collapsed / expanded / focus | keyboard operable; check `aria-expanded` |
| **Info-box (icon+title)** | `.pbmit-ihbox-style-15` | theme ihbox | default / hover | hover in reduced-motion block |
| **Footer** | `.site-footer pbmit-footer-style-1` | theme footer | link hover / focus | 3px gold top border signature; tap targets 44px; `text-transform:none` |
| **Eyebrow / subtitle** | `.pbmit-subtitle` + ledger `::before` | theme subtitle | — | gold ledger stroke signature; AA-checked across surfaces |
| **Floating WhatsApp** | `.pfg-whatsapp-float` | — | default / hover / focus | z-index `--pfg-float`; logic in `initWhatsAppFloat` |
| **Breadcrumb / title bar** | `.pbmit-title-bar-wrapper` | theme | — | provides the `<h1>` on inner pages |
| **Modal / popup** | Magnific Popup | `magnific-popup` | open / close | confirm if actually used per page before specifying |

**Enumeration method for the contract:** for each page, list its `pbmit-*` shortcode blocks and `pfg-*` blocks; the union (above) is the component set. Mark which pages instantiate each so the contract notes per-component coverage (e.g. hero/marquee = index only; lead form = contacts only; pricing = services + detail pages).

## JS Safety

**Init order (do not disturb):** libraries → `gsap-animation.js` (sticky header, GSAP titles) → `scripts.js` (Swiper, AOS, counters, menu dropdowns, accordion) → `js/custom.js` (LAST). `custom.js` must remain last so its patches run after theme init.

**Hard "do not touch" list:**
- **Do not edit `scripts.js` or `gsap-animation.js`** (vendor). All behavior changes go in `custom.js`.
- **Do not reorder the `<script>` tags** in any `<head>`/end-of-body — theme code relies on global `$`, `gsap`, `Swiper`, `AOS` being present in order.
- **Do not re-init or destroy theme widgets.** Specifically: never call Swiper `autoplay.stop()/start()` on the marquee (`disableOnInteraction:true` makes a stop→start permanently halt it) — change only `swiper.params.speed` (documented at `custom.js:113-146`).
- **Do not mutate the DOM that theme widgets bind to** before/around their init — i.e. no header/slider/menu markup injection or restructuring (this is why runtime header injection is rejected above).
- **Do not change the lead-form→WhatsApp flow**: `WA_NUMBER`, message assembly, consent validation, `wa.me` deep link, `.pfg-form-status` feedback (`custom.js:72-111`) are logic, not UI. Style the form, never its behavior.

**Safe-change patterns (keep using):**
- New behavior = a new `initX()` inside the single IIFE, called from the `DOMContentLoaded` block, **early-returning if its target is absent** (safe on all 11 pages).
- **Vanilla JS only** — no jQuery in `custom.js`, even though it's loaded.
- **Idempotent DOM patches** — check before writing (`if (!svg.getAttribute('aria-hidden'))`), so late/repeat theme re-inits don't clobber.
- **Poll for late widgets** (`setInterval` 100ms × ~10s) when reaching into Swiper/GSAP-managed elements, matching `initMarqueeSpeed`.
- **Loose end to consider:** `initSwiperA11y` is defined (`custom.js:180`) but never called. The a11y pass may wire it in — but only after verifying it doesn't fight the slider; treat as a deliberate, tested change, not a drive-by.

## Build Order

Dependency-ordered so each stage rests on the one before. Each stage ends with cross-device + a11y verification via Playwright (the only QA available — no automated tests exist).

1. **Tokens first (foundation).** Consolidate and complete the `:root` token sheet in `custom.css` (color/spacing/type/radii/shadow/z-index/motion). Everything downstream references these. *Why first:* primitives have no dependencies; components depend on them. No visual change should ship yet beyond wiring values. **Gate:** token table matches brand; contrast of text/semantic colors verified AA.
2. **Primitives — type, color, spacing applied to base elements.** Apply the type scale (`clamp()`), body/heading colors, link styling, focus-visible ring, section vertical rhythm (`--pfg-section-y`). *Depends on:* stage 1. *Why here:* establishes the visual baseline every component inherits; catches Russian text-transform issues globally. **Gate:** headings/body legible and consistent across all 11 pages at 3 breakpoints.
3. **Components.** Buttons → inputs/forms → cards → nav/header → footer → hero/pricing/FAQ/info-box → floating WhatsApp. Specify and implement each per the inventory, with all states (hover/focus/active/disabled). *Depends on:* stages 1–2. Order within: buttons and inputs first (highest reuse, conversion-critical), chrome (nav/footer) next, page-specific blocks last. **Gate:** each component matches contract states; no new `!important` introduced; `@layer` used for new self-contained components.
4. **Page-level conversion blocks.** Tune the high-value composites — hero, pricing/tariffs, FAQ, footer CTA, contacts lead-form *presentation* — for visual strength and alignment, page by page, reusing the now-stable components. *Depends on:* stage 3. **Gate:** conversion blocks visually strong and aligned desktop/tablet/mobile; lead-form behavior unchanged.
5. **Accessibility pass.** Focus order, ARIA, contrast re-check on final colors, tap targets (44px), reduced-motion scope review, keyboard operability of accordion/menu/forms; consider wiring `initSwiperA11y`. *Depends on:* stages 3–4 (final markup/colors must exist to audit). **Gate:** axe/Lighthouse a11y ≥ current baseline (no regression); known header search target-size flag explicitly re-confirmed as accepted or fixed.
6. **Cross-device verification + chrome-drift audit.** Full Playwright sweep at desktop/tablet/mobile across all 11 pages; run the chrome-drift audit script to confirm header/footer/`<head>` consistency; screenshot set + local-check command list for the final review. *Depends on:* all prior. **Gate:** no broken wrapping/overflow; chrome audit passes; screenshots captured.

**Dependency rationale:** tokens → primitives → components → pages is strict bottom-up — a component can't be styled before its tokens exist, and a page composite can't be tuned before its components are stable. A11y comes after components/pages because contrast and focus-order audits need final colors and final markup. Cross-device verification is last because it validates the integrated result. The chrome-drift audit script (stage 6, but buildable anytime) is the safety net specifically for the no-include 11-page risk.

## Confidence

| Area | Confidence | Reason |
|------|------------|--------|
| Token layer placement (custom.css `:root`, last-loaded) | **HIGH** | Directly follows the documented load order (`index.html:30-54`) and matches the existing `--pfg-*` block; CSS load-order semantics are deterministic. |
| Token taxonomy (2-tier, clamp type, breakpoint-as-convention) | **HIGH** | Standard design-token practice; `var()`-in-`@media` limitation is a well-established CSS fact. |
| `@layer` as the `!important`-reduction tool | **MEDIUM** | Cascade-layer semantics are well-defined and broadly supported, but the *layered vs. unlayered beats theme* nuance means adoption must be incremental and tested; can't layer vendor files without touching `<link>`s. Recommend piloting on one new component before broad use. |
| custom.css reorganization (ToC + component blocks, keep journal) | **HIGH** | Low-risk documentation/sectioning; explicitly avoids source-order churn that could shift equal-specificity cascade. |
| 11-page consistency: CSS-first + audit script, reject header JS injection | **HIGH** | Empirically grounded (header/footer hashes measured); JS-binding risk to header is concrete (`initMobileMenu`/GSAP sticky bind at DOMContentLoaded). |
| Footer JS-injection as last resort | **MEDIUM** | Technically feasible and lower-risk than header, but FOUC/SEO tradeoffs make it situational; flagged as not-recommended unless drift becomes unmanageable. |
| JS safety / do-not-touch list | **HIGH** | Taken directly from documented anti-patterns and conventions (marquee speed, vanilla-only, idempotency, early-return). |
| Build order & dependencies | **HIGH** | Bottom-up token→component→page→a11y→verify is the conventional and dependency-correct sequence; matches the audit-first project decision. |

**Gaps for phase-specific research:** (1) exact per-page component coverage (which pages have pricing/FAQ/modal) should be enumerated during the audit phase by walking each page, not assumed; (2) a one-component `@layer` pilot should validate the cascade behavior against the real theme before committing to broad layer migration; (3) confirm Magnific Popup modal is actually instantiated anywhere before writing modal contract rules.
