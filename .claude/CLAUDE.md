<!-- GSD:project-start source:PROJECT.md -->

## Project

**taxpfg.kz — Production UI Polish**

taxpfg.kz — статический сайт-визитка бухгалтерско-налоговой консалтинговой фирмы (PrimeFinance Group) в Казахстане. 11 HTML-страниц на базе коммерческой темы GudFin (PBMIT) с наложенным премиальным слоем «чернила + золото» (`css/custom.css`, `css/base.css`, `js/custom.js`). Цель текущего milestone — провести полный UI-аудит и довести визуал до production-уровня, не трогая бизнес-логику, формы и user flows.

**Core Value:** Сайт должен выглядеть дорого, единообразно и убедительно на desktop/tablet/mobile, а ключевые conversion-блоки (hero, тарифы, формы, CTA) — чисто конвертировать посетителя в лид. Если всё остальное провалится — это должно работать.

### Constraints

- **Tech stack**: правки только в `css/custom.css`, `css/base.css`, `js/custom.js` — vendor/theme read-only — чтобы не сломать обновляемость темы и не порождать регрессии
- **No-build**: нельзя вводить сборку/бандлер; всё работает открытием HTML в браузере
- **Logic-safe**: бизнес-логика, формы→WhatsApp, аналитика, роутинг, JSON-LD не должны измениться по поведению
- **Cross-device**: каждое изменение проверяется на desktop, tablet, mobile
- **A11y-floor**: Lighthouse/accessibility не должны стать хуже текущего baseline
- **Duplication**: header/footer на 11 страницах — общие правки придётся вносить согласованно во все файлы (нет include-механизма)

<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->

## Technology Stack

## Languages

- HTML5 - 11 static pages at repo root (`index.html`, `about.html`, `services.html`, `accounting.html`, `accounting-recovery.html`, `taxes.html`, `consulting.html`, `registration.html`, `contacts.html`, `privacy.html`, `404.html`)
- CSS3 - styling under `css/` (custom layer + vendored theme)
- JavaScript (ES5-style, browser, no modules) - behavior under `js/`
- JSON-LD - inline structured data (`schema.org` `AccountingService`) embedded in each page `<head>`, e.g. `index.html:24`
- XML - sitemap (`sitemap.xml`)

## Runtime

- Browser only. This is a pure static website served directly as files. There is **NO server-side runtime**, no Node, no PHP, no backend process.
- None. There is **no `package.json`**, no lockfile, no dependency manifest of any kind. All third-party libraries are vendored (committed) into `css/` and `js/`.

## Build System

- No `package.json`, `webpack`, `vite`, `gulp`, `rollup`, or similar config anywhere.
- HTML pages reference assets directly by relative path (`css/...`, `js/...`).
- Vendored libraries are pre-minified files committed to the repo.
- Deployment = copy files to a static host. Editing = edit the file, refresh the browser.
- `css/custom.css` - PrimeFinance Group overrides (loaded last in `<head>`, e.g. `index.html:54`)
- `css/base.css` - base layer (theme-level, loaded before `style.css`)
- `js/custom.js` - project behavior: mobile menu, lead form → WhatsApp, marquee tuning

## Frameworks & Vendored Libraries

- Bootstrap `5.2.0-beta1` - `css/bootstrap.min.css` + `js/bootstrap.min.js` (grid, layout, components)
- GudFin HTML theme - `css/style.css`, `css/base.css`, `css/responsive.css`, `css/shortcode.css`, `css/pbmit_gudfin.css` (PBMIT/Pbminfotech commercial theme this site is based on)
- jQuery `3.7.1` - `js/jquery.min.js` (DOM/ajax base for theme plugins)
- Popper `2.9.2` (`@popperjs/core`) - `js/popper.min.js` (Bootstrap tooltip/dropdown positioning)
- Bootstrap JS `5.2.0-beta1` - `js/bootstrap.min.js`
- Waypoints `4.0.1` - `js/jquery.waypoints.min.js` (scroll triggers)
- jQuery Appear - `js/jquery.appear.js` (element-in-viewport)
- Numinate - `js/numinate.min.js` (animated number counters)
- Swiper `7.3.3` - `js/swiper.min.js` + `css/swiper.min.css` (sliders, services marquee)
- Magnific Popup `1.1.0` (2016-02-20) - `js/jquery.magnific-popup.min.js` + `css/magnific-popup.css` (lightbox/modal)
- Circle Progress - `js/circle-progress.js` (radial progress widgets)
- The Final Countdown `2.2.0` - `js/jquery.countdown.min.js` (countdown timer)
- AOS - `js/aos.js` + `css/aos.css` (animate-on-scroll)
- GSAP `3.10.4` - `js/gsap.js` plus plugins `js/ScrollTrigger.js`, `js/SplitText.js` and the theme glue `js/gsap-animation.js` (scroll/text animations)
- Theia Sticky Sidebar - `js/theia-sticky-sidebar.js` (sticky sidebar widgets)
- Chart.js `4.5.0` - `js/chart.js` (charts; vendored, present in theme)
- `js/scripts.js` - GudFin theme glue (initializes the above plugins)
- `js/email-decode.min.js` - Cloudflare email obfuscation decoder (vendored, theme artifact)
- `js/custom.js` - the only hand-written script. Loaded last (`index.html:1057`).

## Icon Fonts

- Font Awesome - `fonts/fontawesome-webfont.{eot,ttf,woff,woff2}` via `css/fontawesome.css`
- Themify Icons - `fonts/themify.{eot,ttf,woff}` via `css/themify-icons.css`
- Pbminfotech base icons - `fonts/pbminfotech-base-icons.{eot,ttf,woff,woff2}` via `css/pbminfotech-base-icons.css`
- Pbmit GudFin icons - `fonts/pbmit_gudfin.{eot,ttf,woff,woff2}` via `css/pbmit_gudfin.css`

## Text Fonts

- Be Vietnam Pro - body text (`--pbmit-body-typography-font-family`)
- Plus Jakarta Sans - headings and buttons
- Roboto - imported (theme default)
- Montserrat - referenced as a fallback family in `css/base.css:272` (not explicitly imported)

## Configuration Files

- `robots.txt` - allows all crawlers, points to sitemap (`Sitemap: https://taxpfg.kz/sitemap.xml`)
- `sitemap.xml` - 10 URLs with `lastmod` 2026-06-20, `changefreq` monthly, priorities 0.3–1.0 (`accounting-recovery.html` and `404.html` are not listed)
- `.gitignore` - ignores `node_modules/`, OS junk, logs, Playwright/screenshot audit artifacts, root-level images, and Python bytecode
- Favicon: `images/fevicon.png` referenced via `<link rel="shortcut icon">` (`index.html:26`)

## Platform Requirements

- Any text editor plus a browser. Optionally a static file server (e.g. `python -m http.server`) so relative paths and the Google Fonts/Maps requests resolve over HTTP.
- Any static host / CDN capable of serving plain files (the canonical/OpenGraph URLs and sitemap target `https://taxpfg.kz/`). No application server, database, or runtime environment required.

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

- `css/custom.css` — all bespoke styling (loaded last, overrides the theme)
- `css/base.css` — vendor theme base (design tokens / CSS custom properties live here; treated as read-only)
- `js/custom.js` — all bespoke behavior (vanilla JS, IIFE)

## Naming Patterns

- `pfg-*` — project-authored elements and utilities. PFG = PrimeFinance Group. Examples: `.pfg-logo`, `.pfg-card`, `.pfg-section`, `.pfg-prose`, `.pfg-lead`, `.pfg-form`, `.pfg-consent`, `.pfg-form-status`, `.pfg-whatsapp-float`, `.pfg-steps`, `.pfg-sr-only`, `.pfg-cta-actions`.
- `pbmit-*` — vendor theme classes (PBM Infotech, the theme author). Project CSS *targets* these to override, but never owns them. Examples: `.pbmit-btn`, `.pbmit-subtitle`, `.pbmit-title-bar-wrapper`, `.pbmit-slider-one`.
- Bootstrap utility classes (`.row`, `.col-md-6`, `.container`, `.form-control`, `.form-select`) come from `css/bootstrap.min.css` and are used as-is in markup.
- `--pbmit-*` — theme design tokens, defined in `css/base.css:21-49` (brand colors, typography, breakpoint). Treated as the source of truth for brand values; referenced via `var()`, occasionally overridden in `custom.css` (e.g. `--pbmit-body-typography-color` darkened for contrast at `css/custom.css:122`).
- `--pfg-*` — premium-layer tokens, defined in `css/custom.css:284-302`. These hold the "ink + gold" theme values (see below). Brand colors are NOT redefined here — `--pfg-*` tokens reuse the same hex values with project-specific semantic names.

## Code Style

- No automated formatter (no Prettier, no ESLint, no `.editorconfig` detected).
- Indentation is **tabs** throughout `css/custom.css` and `js/custom.js`.
- CSS: one selector block per rule, properties on their own lines for multi-property rules; short utilities collapsed onto one line (`.pfg-muted{ opacity:.85; }` at `css/custom.css:56`).
- Opening brace on the same line as the selector. Space inside braces for single-line rules.

## CSS Architecture — the custom layer

- Use `!important` only when overriding a vendor rule that cannot otherwise be beaten (theme media queries in `responsive.css`, inline-ish high-specificity selectors).
- Document *why* each override is needed in the section comment, including the vendor file/line being overridden (e.g. `css/custom.css:651-652` cites `responsive.css:145`).
- Prefer reusing the project's own `--pfg-*` tokens inside the overriding rule.
- New project-owned elements (`.pfg-*`) generally do NOT need `!important` — it is reserved for fighting the theme.
- Media-query gating is used heavily and explained. The "glass header" is gated to `min-width:1201px` (`css/custom.css:390`) specifically because below that the theme turns the menu into a fixed off-canvas panel and any `backdrop-filter` on an ancestor collapses `height:100%` (documented at `css/custom.css:382-389`). This is a key constraint: **decorative effects using `filter`/`backdrop-filter`/`transform` must not be applied to ancestors of the mobile off-canvas menu.**
- Selectors target the vendor class plus a contextual parent to limit reach (e.g. `.pfg-prose p a:not(.pbmit-btn)` at `css/custom.css:268` underlines inline prose links but excludes buttons and contact cards).
- `--pfg-ink: #16222d` (brand dark / "чернила"), `--pfg-ink-deep: #0f1820`
- `--pfg-gold: #ecab23` (brand gold), `--pfg-gold-deep: #d6960f` (hover), `--pfg-gold-ink: #7a560a` (gold-colored *text* on light backgrounds, chosen to clear WCAG AA ≥5.4:1)
- Hairlines, paper-warm background (`#f6f4ef` replacing the theme's cold `#ecf0f4`), a shadow scale (`--pfg-shadow-sm/md/btn/btn-h`), radius scale (`--pfg-radius`, `--pfg-radius-sm`), and a shared easing curve `--pfg-ease: cubic-bezier(.22,.61,.36,1)` with two transition presets (`--pfg-tf-fast`, `--pfg-tf`).
- Signature motif: a gold "ledger stroke" (`::before` rule) before eyebrow subtitles, and a 3px gold top border on the footer (`css/custom.css:512`). Reuse these tokens for any new premium-layer styling rather than hardcoding hex values.
- Contrast fixes change color tokens, never brand identity — the gold fill stays `#ecab23`; only *text* color or *text-on-gold* is darkened (`css/custom.css:128-139`).
- Tap targets: interactive glyphs get `min-width/min-height: 44px` hit zones (`css/custom.css:164-170`, footer menu `css/custom.css:565-571`) per WCAG 2.5.5.
- `.pfg-sr-only` (`css/custom.css:941-951`) is the standard visually-hidden pattern for screen-reader-only content (used for the index page `<h1>`).
- **`prefers-reduced-motion` is scoped, never universal** (`css/custom.css:332-345`). A prior universal `*{transition-duration:.001ms!important}` killer was removed because it broke the theme's Swiper/marquee/GSAP animations (which carry the brand identity). The current rule disables *only* the decorative micro-interactions added by the premium layer (card/button lift, nav underline growth, ihbox hover). When adding motion, if it is decorative, add it to this reduced-motion block; if it is brand identity, leave it out. History documented at `css/custom.css:315-331` and commit `830a769`.

## JavaScript Conventions — `js/custom.js`

- Single file-scoped IIFE wrapping everything: `(function () { 'use strict'; ... })();` (`js/custom.js:1-2`, `:202`).
- `'use strict'` always on.
- One `DOMContentLoaded` listener that calls a set of small, single-purpose `initX()` functions (`js/custom.js:6-13`).
- Each `initX()` guards for the absence of its target element and returns early (`if (!toggle || !nav) return;` at `js/custom.js:22`) — functions are safe to run on pages where their feature is absent.
- A block comment precedes each function explaining the *why* (vendor behavior being worked around), in Russian, often citing the theme constraint (e.g. the marquee speed comment at `js/custom.js:113-130` explains why `autoplay.stop()/start()` must not be called).

## HTML / Markup Conventions

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

- Format: `type(scope): описание на русском`
- Types in use: `feat`, `fix`, `chore`, `wip`.
- Scopes seen: `a11y`, `ui`, `images`, `a11y+layout`. Scope is optional.
- Descriptions are Russian, lowercase-leading, often with an em dash introducing detail: `fix(a11y): точечный prefers-reduced-motion вместо универсального гасителя`.
- Some historical commits use a `Этап N (...)` ("Stage N") prefix instead of conventional type — older convention, now superseded by conventional commits.
- Per global rules, do not commit unless explicitly asked; never commit secrets.

<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

## System Overview

```text

```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Page documents | Full standalone HTML — own `<head>`, header, content, footer, script tags | `index.html`, `about.html`, `services.html`, `accounting.html`, `accounting-recovery.html`, `taxes.html`, `consulting.html`, `registration.html`, `contacts.html`, `privacy.html`, `404.html` |
| Theme base tokens | CSS custom properties (`--pbmit-*`), typography, helpers, header/search base | `css/base.css` |
| Theme core styles | GudFin theme layout, shortcodes, components | `css/style.css`, `css/shortcode.css` |
| Theme responsive | Breakpoint rules for theme | `css/responsive.css` |
| Custom override layer | All PrimeFinance edits on top of GudFin (premium "ink + gold" look, a11y, `.pfg-*` utilities) | `css/custom.css` |
| Theme JS init | Swiper sliders, AOS, circle progress, back-to-top, accordion, menu dropdowns, charts | `js/scripts.js` |
| Theme animation | GSAP title/scroll animation, sticky header | `js/gsap-animation.js` |
| Custom JS layer | Mobile menu toggle, WhatsApp float + lead form, marquee speed fix, a11y patches | `js/custom.js` |

## Pattern Overview

- Every page is fully self-contained: header markup, nav, footer, and the full `<script>`/`<link>` list are **copy-pasted into all 11 HTML files** (no server-side or build-time includes).
- Vendor theme files are treated as read-only; all customization lives in two append-only files: `css/custom.css` and `js/custom.js`.
- Customization works by cascade override (CSS loaded last wins) and post-init DOM patching (JS runs after theme JS).
- Forms have no backend — the lead form composes a WhatsApp deep link instead.

## Layers

- Purpose: Deliver content; each page is the unit of routing (filename = URL).
- Location: repo root (`*.html`)
- Contains: identical `<head>`, identical `<header class="site-header pbmit-header-style-1">`, page-specific `<main id="content">`, identical `<footer class="site-footer pbmit-footer-style-1">`, identical script block.
- Depends on: all `css/*` and `js/*` assets via relative paths.
- Purpose: Bootstrap grid + GudFin theme look.
- Location: `css/bootstrap.min.css`, `css/style.css`, `css/shortcode.css`, `css/responsive.css`, `css/base.css`, icon/plugin CSS.
- Used by: every page; **not edited**.
- Purpose: Brand the theme (PrimeFinance ink+gold), add `.pfg-*` content utilities, fix a11y/contrast, patch theme bugs (e.g. missing select-arrow image).
- Location: `css/custom.css` (951 lines, loaded last).
- Depends on: theme tokens (`var(--pbmit-global-color)` etc.) defined in `css/base.css`.
- Purpose: interactive widgets (sliders, counters, charts, scroll animation, sticky header).
- Location: `js/scripts.js`, `js/gsap-animation.js`, plus jQuery/GSAP/Swiper/AOS libraries; **not edited**.
- Purpose: behaviour the theme lacks or gets wrong — mobile menu handler, floating WhatsApp button, lead-form→WhatsApp, marquee slowdown, accessibility patches.
- Location: `js/custom.js` (loaded last).

## Data Flow

### Primary Request Path (page view)

### Lead form flow (no backend)

- No client-side state framework. Transient UI state is held as DOM classes (e.g. `.active` on `#site-navigation`, `body.pfg-menu-open`) and Swiper/AOS instance objects attached to elements (`el.swiper`).

## Key Abstractions

- Purpose: a route + its content.
- Examples: `index.html`, `services.html`, `contacts.html`.
- Pattern: duplicated chrome (head/header/footer/scripts) + unique `<main id="content">`.
- Purpose: reusable content blocks for inner pages independent of theme shortcodes.
- Examples: `.pfg-section`, `.pfg-card`, `.pfg-grid`, `.pfg-steps`, `.pfg-form`, `.pfg-lead` defined in `css/custom.css:62-90`.
- Pattern: prefix-namespaced (`pfg-` = PrimeFinance Group) to avoid colliding with theme `pbmit-` classes.
- Purpose: GudFin theme structural/visual blocks.
- Examples: `pbmit-slider-area`, `pbmit-title-bar-wrapper`, `pbmit-header-style-1`, `pbmit-footer-style-1`.
- Pattern: vendor namespace; styled by theme CSS, only overridden (never authored) in `custom.css`.

## Entry Points

- Location: repo root `*.html`.
- Triggers: direct HTTP request / link navigation.
- Responsibilities: load shared assets, render its `<main id="content">`.
- Location: `js/custom.js:6`.
- Triggers: every page after DOM parse.
- Responsibilities: `initMobileMenu`, `initWhatsAppFloat`, `initLeadForm`, `initMarqueeSpeed`, `initSvgAria`, `initSearchA11y`.
- Location: `js/scripts.js:1`.
- Triggers: every page once jQuery is loaded.
- Responsibilities: theme widget initialization.

## Architectural Constraints

- **No build step:** files are edited and shipped directly; there is no compilation, minification, or include mechanism. Any markup shared across pages (header, footer, nav, script list) must be edited in all 11 files by hand.
- **Vendor files are read-only:** `css/base.css`, `css/style.css`, `css/shortcode.css`, `css/responsive.css`, `js/scripts.js`, `js/gsap-animation.js` and all libraries are theme-owned. Changes go in `css/custom.css` / `js/custom.js` only. This is stated explicitly at `css/custom.css:1-4` and `js/custom.js:113-130`.
- **Load order is load-bearing:** `custom.css` must remain the last stylesheet and `custom.js` the last script, or overrides stop winning. See `index.html:54` and `index.html:1057`.
- **Single-threaded, jQuery-global:** theme code is one big jQuery IIFE relying on the global `$`/`jQuery`, plus globals `gsap`, `Swiper`, `AOS`. `custom.js` deliberately avoids jQuery and uses vanilla DOM.
- **Race with theme init:** Swiper/GSAP may init on `DOMContentLoaded` or `window.load`. `custom.js` polls on an interval to re-apply fixes (e.g. `initMarqueeSpeed` at `js/custom.js:131-146`) rather than assuming a single ready moment.

## Anti-Patterns

### Editing vendor theme files directly

### Calling Swiper autoplay stop/start to change marquee speed

### Assuming markup edits propagate across pages

## Error Handling

- Every `init*` in `js/custom.js` early-returns when its target element is absent (e.g. `if (!toggle || !nav) return;` at `js/custom.js:22`), so the same script is safe on all pages regardless of which elements exist.
- Idempotent DOM patches: a11y fixes check before writing (`if (!svg.getAttribute('aria-hidden'))` at `js/custom.js:155`) so repeated/late runs don't clobber state.
- Form validation surfaces user-facing messages via `.pfg-form-status` rather than throwing (`js/custom.js:82-88`).

## Cross-Cutting Concerns

<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
