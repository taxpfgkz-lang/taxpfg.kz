# Coding Conventions

**Analysis Date:** 2026-06-25

This is a **static HTML site** built on the purchased "GudFin" HTML theme. There is no build system, no transpiler, no framework. The custom layer — the only code authored by this project — lives in three files:

- `css/custom.css` — all bespoke styling (loaded last, overrides the theme)
- `css/base.css` — vendor theme base (design tokens / CSS custom properties live here; treated as read-only)
- `js/custom.js` — all bespoke behavior (vanilla JS, IIFE)

The governing rule across the whole custom layer: **never edit vendor theme files** (`base.css`, `style.css`, `shortcode.css`, `responsive.css`, `scripts.js`, etc.). All deviations from the theme are layered on top via `custom.css` / `custom.js`. This is stated explicitly at `css/custom.css:2-3` and repeated in nearly every section header.

## Naming Patterns

**CSS classes — two namespaces:**
- `pfg-*` — project-authored elements and utilities. PFG = PrimeFinance Group. Examples: `.pfg-logo`, `.pfg-card`, `.pfg-section`, `.pfg-prose`, `.pfg-lead`, `.pfg-form`, `.pfg-consent`, `.pfg-form-status`, `.pfg-whatsapp-float`, `.pfg-steps`, `.pfg-sr-only`, `.pfg-cta-actions`.
- `pbmit-*` — vendor theme classes (PBM Infotech, the theme author). Project CSS *targets* these to override, but never owns them. Examples: `.pbmit-btn`, `.pbmit-subtitle`, `.pbmit-title-bar-wrapper`, `.pbmit-slider-one`.
- Bootstrap utility classes (`.row`, `.col-md-6`, `.container`, `.form-control`, `.form-select`) come from `css/bootstrap.min.css` and are used as-is in markup.

**CSS custom properties — two namespaces:**
- `--pbmit-*` — theme design tokens, defined in `css/base.css:21-49` (brand colors, typography, breakpoint). Treated as the source of truth for brand values; referenced via `var()`, occasionally overridden in `custom.css` (e.g. `--pbmit-body-typography-color` darkened for contrast at `css/custom.css:122`).
- `--pfg-*` — premium-layer tokens, defined in `css/custom.css:284-302`. These hold the "ink + gold" theme values (see below). Brand colors are NOT redefined here — `--pfg-*` tokens reuse the same hex values with project-specific semantic names.

**CSS modifier convention:** BEM-ish suffix with double dash for variants — `.pfg-section--alt`, `.pfg-logo--dark`. State classes use `is-` prefix: `.pfg-form-status.is-error`, `.pfg-form-status.is-ok`.

**JS:** `camelCase` functions and variables (`initMobileMenu`, `initLeadForm`, `openMenu`). Module-level constants in `UPPER_SNAKE_CASE` (`WA_NUMBER` at `js/custom.js:4`, `MARQUEE_SPEED` at `js/custom.js:132`, `MAX_TICKS`).

## Code Style

**Formatting:**
- No automated formatter (no Prettier, no ESLint, no `.editorconfig` detected).
- Indentation is **tabs** throughout `css/custom.css` and `js/custom.js`.
- CSS: one selector block per rule, properties on their own lines for multi-property rules; short utilities collapsed onto one line (`.pfg-muted{ opacity:.85; }` at `css/custom.css:56`).
- Opening brace on the same line as the selector. Space inside braces for single-line rules.

**Linting:** None configured. Quality is enforced by manual review and the UI/a11y audit process (see `TESTING.md`).

## CSS Architecture — the custom layer

**Load order is load-bearing.** `css/custom.css` is the **last** stylesheet linked in every page `<head>` (`registration.html:55`, after `base.css`, `style.css`, `responsive.css`). The entire override strategy depends on this. If `custom.css` is moved earlier, the cascade breaks. Never reorder the `<link>` tags.

**`!important` usage (~59 occurrences):** Used deliberately and pervasively to win the cascade against the vendor theme, which itself ships high-specificity and media-query rules. The convention:
- Use `!important` only when overriding a vendor rule that cannot otherwise be beaten (theme media queries in `responsive.css`, inline-ish high-specificity selectors).
- Document *why* each override is needed in the section comment, including the vendor file/line being overridden (e.g. `css/custom.css:651-652` cites `responsive.css:145`).
- Prefer reusing the project's own `--pfg-*` tokens inside the overriding rule.
- New project-owned elements (`.pfg-*`) generally do NOT need `!important` — it is reserved for fighting the theme.

**Scoping overrides:** Overrides are scoped as narrowly as possible to avoid collateral damage:
- Media-query gating is used heavily and explained. The "glass header" is gated to `min-width:1201px` (`css/custom.css:390`) specifically because below that the theme turns the menu into a fixed off-canvas panel and any `backdrop-filter` on an ancestor collapses `height:100%` (documented at `css/custom.css:382-389`). This is a key constraint: **decorative effects using `filter`/`backdrop-filter`/`transform` must not be applied to ancestors of the mobile off-canvas menu.**
- Selectors target the vendor class plus a contextual parent to limit reach (e.g. `.pfg-prose p a:not(.pbmit-btn)` at `css/custom.css:268` underlines inline prose links but excludes buttons and contact cards).

**Design tokens — the "ink + gold" premium theme** (`css/custom.css:283-302`):
- `--pfg-ink: #16222d` (brand dark / "чернила"), `--pfg-ink-deep: #0f1820`
- `--pfg-gold: #ecab23` (brand gold), `--pfg-gold-deep: #d6960f` (hover), `--pfg-gold-ink: #7a560a` (gold-colored *text* on light backgrounds, chosen to clear WCAG AA ≥5.4:1)
- Hairlines, paper-warm background (`#f6f4ef` replacing the theme's cold `#ecf0f4`), a shadow scale (`--pfg-shadow-sm/md/btn/btn-h`), radius scale (`--pfg-radius`, `--pfg-radius-sm`), and a shared easing curve `--pfg-ease: cubic-bezier(.22,.61,.36,1)` with two transition presets (`--pfg-tf-fast`, `--pfg-tf`).
- Signature motif: a gold "ledger stroke" (`::before` rule) before eyebrow subtitles, and a 3px gold top border on the footer (`css/custom.css:512`). Reuse these tokens for any new premium-layer styling rather than hardcoding hex values.

**Sectioned, heavily-commented structure:** `custom.css` is organized into numbered, dated "Этап" (stage) blocks with banner comments (`/* ===== ЭТАП N — ... (date) ===== */`). Each block states what changed, the contrast/measurement rationale, and which vendor rule it overrides. **When adding new styles, append a new dated section comment in the same style** rather than scattering edits. Comments are in Russian and frequently cite exact contrast ratios and DOM measurements (e.g. `css/custom.css:117-121`, `css/custom.css:531-540`).

**Accessibility conventions in CSS:**
- Contrast fixes change color tokens, never brand identity — the gold fill stays `#ecab23`; only *text* color or *text-on-gold* is darkened (`css/custom.css:128-139`).
- Tap targets: interactive glyphs get `min-width/min-height: 44px` hit zones (`css/custom.css:164-170`, footer menu `css/custom.css:565-571`) per WCAG 2.5.5.
- `.pfg-sr-only` (`css/custom.css:941-951`) is the standard visually-hidden pattern for screen-reader-only content (used for the index page `<h1>`).
- **`prefers-reduced-motion` is scoped, never universal** (`css/custom.css:332-345`). A prior universal `*{transition-duration:.001ms!important}` killer was removed because it broke the theme's Swiper/marquee/GSAP animations (which carry the brand identity). The current rule disables *only* the decorative micro-interactions added by the premium layer (card/button lift, nav underline growth, ihbox hover). When adding motion, if it is decorative, add it to this reduced-motion block; if it is brand identity, leave it out. History documented at `css/custom.css:315-331` and commit `830a769`.

**Known accepted exception:** the mobile header search tap-target flag at `css/custom.css:141-151` is intentionally left unfixed. The theme's absolutely-positioned hamburger overlaps the search icon, and cleanly separating them would require rewriting the off-canvas layout (a known trap zone). Documented as a known theme limitation; do not "fix" it without revisiting that decision.

## JavaScript Conventions — `js/custom.js`

**No jQuery in the custom layer.** Although the theme bundles and depends on jQuery (`js/jquery.min.js` loaded before `custom.js` at `registration.html:521`), `js/custom.js` is **vanilla JS only** — `document.querySelector`, `addEventListener`, `classList`, `forEach`. Match this: do not introduce `$(...)` into the custom file.

**Structure:**
- Single file-scoped IIFE wrapping everything: `(function () { 'use strict'; ... })();` (`js/custom.js:1-2`, `:202`).
- `'use strict'` always on.
- One `DOMContentLoaded` listener that calls a set of small, single-purpose `initX()` functions (`js/custom.js:6-13`).
- Each `initX()` guards for the absence of its target element and returns early (`if (!toggle || !nav) return;` at `js/custom.js:22`) — functions are safe to run on pages where their feature is absent.
- A block comment precedes each function explaining the *why* (vendor behavior being worked around), in Russian, often citing the theme constraint (e.g. the marquee speed comment at `js/custom.js:113-130` explains why `autoplay.stop()/start()` must not be called).

**Event handling:** Native `addEventListener`. Forms call `e.preventDefault()` then handle in JS (`js/custom.js:78`). Keyboard handling for Escape-to-close (`js/custom.js:51-53`).

**Idempotency convention:** A11y patches that mutate vendor DOM check before writing, so re-runs and theme re-inits don't clobber: `if (!svg.getAttribute('aria-hidden'))` (`js/custom.js:155`), same for `aria-label` (`js/custom.js:169`). Stated as "Идемпотентно" in comments.

**Polling for late-initialized theme widgets:** Where the theme initializes Swiper on either `DOMContentLoaded` or `window.load`, the custom layer polls with `setInterval` at 100ms for ~10s (`MAX_TICKS = 100`) then clears the timer — see `initMarqueeSpeed` (`js/custom.js:131-146`) and `initSwiperA11y` (`js/custom.js:180-200`). This is the established pattern for reaching into theme-managed widgets.

**Static-site form pattern:** There is no backend. `.pfg-form` submissions are intercepted, validated (consent checkbox), serialized into a Russian-language message, and opened in WhatsApp via `https://wa.me/<number>?text=...` (`js/custom.js:72-111`). The phone number is the single constant `WA_NUMBER` at `js/custom.js:4`. Status feedback is written to `.pfg-form-status` with `is-error`/`is-ok` classes.

Note: `initSwiperA11y` is defined (`js/custom.js:180`) but **not** called from the `DOMContentLoaded` block (`js/custom.js:6-13`). Flagged in `CONCERNS.md`.

## HTML / Markup Conventions

**Language:** `<html lang="ru">` on every page (`registration.html:1`). All user-facing content is Russian. Page wrapper `<div class="page-wrapper" id="page">`.

**Document head:** Each page carries a full SEO block — `<title>`, `meta description`, `meta robots`, canonical link, OpenGraph + Twitter card tags, and one or more `application/ld+json` blocks (`AccountingService` org schema + `BreadcrumbList`) — see `registration.html:4-25`. New pages should replicate this block with page-specific values.

**Stylesheet/script order is fixed:** vendor CSS first, `custom.css` last (`registration.html:30-55`); vendor JS first (jQuery → bootstrap → swiper → gsap → `scripts.js`), `custom.js` last (`registration.html:521-555`). Preserve this order.

**Accessibility attributes in markup:**
- Decorative SVGs carry `aria-hidden="true"` inline (`index.html:82`, icon-list bullets); social SVGs without it get patched by `initSvgAria`.
- Icon-only controls have `aria-label` + `title` (`index.html:122`, `:153` menu toggle is `<button type="button" aria-label="Меню">`).
- Live region for form feedback: `<div class="pfg-form-status" role="status" aria-live="polite">` (`contacts.html:273`).
- Forms use real `<label>` wrapping the control, `autocomplete` hints (`name`, `tel`), `required`, and `novalidate` on the form so JS owns validation (`contacts.html:256-263`).
- Exactly one `<h1>` per page. On content pages the title-bar provides it; on `index.html` the slider uses `<h2>` visually and a visually-hidden `<h1 class="pfg-sr-only">` supplies the semantic heading (`index.html:264`). The logo's theme `<h1 class="site-title">` is hidden via CSS (`css/custom.css:622`) to avoid a duplicate H1.

## Russian-Language Content Convention

- All copy, form labels, placeholders, button text, `aria-label`s, and JSON-LD `name`/`areaServed` values are in Russian.
- Several CSS overrides exist *specifically* because the theme's `text-transform: capitalize`/`uppercase` mangles Russian (capitalizing prepositions/conjunctions like "В", "И"). The convention is to set `text-transform: none` and rely on the HTML text already being in correct sentence/Title case — see `css/custom.css:215-218` (footer menu), `:243-258` (buttons), `:865-873` (eyebrows). When the theme imposes a transform on Russian text, override it to `none`.
- Code-side identifiers, class names, file paths, and commit *prefixes* stay in English/Latin; only human-readable descriptions are Russian.

## Comments

- Comments are **in Russian**, explanatory, and dense. They justify *why* a rule exists (the vendor behavior, the measured contrast ratio, the WCAG criterion, the DOM measurement) rather than restating *what* the CSS does.
- Each `custom.css` stage block opens with a banner comment naming the stage number, the tool/context (e.g. "frontend-design", "Lighthouse-аудит"), and a date.
- JS functions are preceded by numbered block comments matching their call order.
- This explanatory style is the standard — preserve it. A future reader should understand the vendor constraint without opening the theme files.

## Commit Message Style

Conventional Commits with **Russian descriptions** (`git log`):
- Format: `type(scope): описание на русском`
- Types in use: `feat`, `fix`, `chore`, `wip`.
- Scopes seen: `a11y`, `ui`, `images`, `a11y+layout`. Scope is optional.
- Descriptions are Russian, lowercase-leading, often with an em dash introducing detail: `fix(a11y): точечный prefers-reduced-motion вместо универсального гасителя`.
- Some historical commits use a `Этап N (...)` ("Stage N") prefix instead of conventional type — older convention, now superseded by conventional commits.
- Per global rules, do not commit unless explicitly asked; never commit secrets.

---

*Convention analysis: 2026-06-25*
