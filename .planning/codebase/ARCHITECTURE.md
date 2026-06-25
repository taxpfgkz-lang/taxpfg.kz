<!-- refreshed: 2026-06-25 -->
# Architecture

**Analysis Date:** 2026-06-25

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│         11 STATIC HTML PAGES (repo root, self-contained)     │
├──────────────────┬──────────────────┬───────────────────────┤
│   index.html     │  service pages   │   info/utility pages  │
│  (homepage)      │  accounting.html │   about / contacts /  │
│                  │  taxes.html …    │   privacy / 404       │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │  every page links the SAME asset files │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     CSS CASCADE (load order)                 │
│  vendor → theme → CUSTOM OVERRIDE LAYER                      │
│  bootstrap.min → fontawesome → pbmit_gudfin → icons →        │
│  swiper → magnific → aos → shortcode → `base.css` →          │
│  `style.css` → `responsive.css` → `css/custom.css` (LAST)    │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                     JS INIT (bottom of <body>)               │
│  jQuery → popper → bootstrap → waypoints → appear →          │
│  numinate → swiper → magnific → circle-progress →            │
│  countdown → aos → gsap → ScrollTrigger → SplitText →        │
│  theia-sticky → `gsap-animation.js` → `scripts.js`           │
│  → `js/custom.js` (LAST, our layer)                          │
└─────────────────────────────────────────────────────────────┘
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

**Overall:** Static multi-page website (MPS) built on a purchased "GudFin" HTML theme, extended by a thin custom override layer. No build system, no bundler, no backend, no `package.json`. Files are served as-is.

**Key Characteristics:**
- Every page is fully self-contained: header markup, nav, footer, and the full `<script>`/`<link>` list are **copy-pasted into all 11 HTML files** (no server-side or build-time includes).
- Vendor theme files are treated as read-only; all customization lives in two append-only files: `css/custom.css` and `js/custom.js`.
- Customization works by cascade override (CSS loaded last wins) and post-init DOM patching (JS runs after theme JS).
- Forms have no backend — the lead form composes a WhatsApp deep link instead.

## Layers

**Page layer (HTML):**
- Purpose: Deliver content; each page is the unit of routing (filename = URL).
- Location: repo root (`*.html`)
- Contains: identical `<head>`, identical `<header class="site-header pbmit-header-style-1">`, page-specific `<main id="content">`, identical `<footer class="site-footer pbmit-footer-style-1">`, identical script block.
- Depends on: all `css/*` and `js/*` assets via relative paths.

**Vendor/theme CSS layer:**
- Purpose: Bootstrap grid + GudFin theme look.
- Location: `css/bootstrap.min.css`, `css/style.css`, `css/shortcode.css`, `css/responsive.css`, `css/base.css`, icon/plugin CSS.
- Used by: every page; **not edited**.

**Custom CSS override layer:**
- Purpose: Brand the theme (PrimeFinance ink+gold), add `.pfg-*` content utilities, fix a11y/contrast, patch theme bugs (e.g. missing select-arrow image).
- Location: `css/custom.css` (951 lines, loaded last).
- Depends on: theme tokens (`var(--pbmit-global-color)` etc.) defined in `css/base.css`.

**Vendor/theme JS layer:**
- Purpose: interactive widgets (sliders, counters, charts, scroll animation, sticky header).
- Location: `js/scripts.js`, `js/gsap-animation.js`, plus jQuery/GSAP/Swiper/AOS libraries; **not edited**.

**Custom JS override layer:**
- Purpose: behaviour the theme lacks or gets wrong — mobile menu handler, floating WhatsApp button, lead-form→WhatsApp, marquee slowdown, accessibility patches.
- Location: `js/custom.js` (loaded last).

## Data Flow

### Primary Request Path (page view)

1. Browser requests a static `*.html` file from the web root (e.g. `index.html`).
2. Browser parses `<head>` and loads CSS in declared order, ending with `css/custom.css` (`index.html:30-54`).
3. Browser renders header (`index.html:62`), `<main id="content">`, footer (`index.html:843`).
4. At end of `<body>` the script block loads libraries then `js/scripts.js` and `js/custom.js` (`index.html:1023-1057`).
5. `js/scripts.js` (jQuery IIFE) initializes Swiper sliders, AOS, counters, back-to-top, menu dropdowns (`js/scripts.js:1`).
6. `js/custom.js` runs on `DOMContentLoaded`, wiring up the mobile menu, WhatsApp button, lead form, and a11y fixes (`js/custom.js:6`).

### Lead form flow (no backend)

1. User submits a `.pfg-form` (e.g. on `contacts.html`).
2. `initLeadForm()` intercepts `submit`, validates the consent checkbox (`js/custom.js:72`).
3. Field values are assembled into a message string and opened as a `https://wa.me/<number>?text=…` deep link (`js/custom.js:95-102`).
4. A status message is shown in `.pfg-form-status`; the form resets.

**State Management:**
- No client-side state framework. Transient UI state is held as DOM classes (e.g. `.active` on `#site-navigation`, `body.pfg-menu-open`) and Swiper/AOS instance objects attached to elements (`el.swiper`).

## Key Abstractions

**Page (HTML file):**
- Purpose: a route + its content.
- Examples: `index.html`, `services.html`, `contacts.html`.
- Pattern: duplicated chrome (head/header/footer/scripts) + unique `<main id="content">`.

**`.pfg-*` content utilities:**
- Purpose: reusable content blocks for inner pages independent of theme shortcodes.
- Examples: `.pfg-section`, `.pfg-card`, `.pfg-grid`, `.pfg-steps`, `.pfg-form`, `.pfg-lead` defined in `css/custom.css:62-90`.
- Pattern: prefix-namespaced (`pfg-` = PrimeFinance Group) to avoid colliding with theme `pbmit-` classes.

**Theme `pbmit-*` components:**
- Purpose: GudFin theme structural/visual blocks.
- Examples: `pbmit-slider-area`, `pbmit-title-bar-wrapper`, `pbmit-header-style-1`, `pbmit-footer-style-1`.
- Pattern: vendor namespace; styled by theme CSS, only overridden (never authored) in `custom.css`.

## Entry Points

**Each HTML page:**
- Location: repo root `*.html`.
- Triggers: direct HTTP request / link navigation.
- Responsibilities: load shared assets, render its `<main id="content">`.

**`js/custom.js` DOMContentLoaded handler:**
- Location: `js/custom.js:6`.
- Triggers: every page after DOM parse.
- Responsibilities: `initMobileMenu`, `initWhatsAppFloat`, `initLeadForm`, `initMarqueeSpeed`, `initSvgAria`, `initSearchA11y`.

**`js/scripts.js` jQuery IIFE:**
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

**What happens:** Tempting to fix a bug or tweak a style in `css/style.css`, `css/base.css`, or `js/scripts.js`.
**Why it's wrong:** These are vendor GudFin files; edits there are unmarked, easy to lose on a theme refresh, and break the clean override boundary the project relies on.
**Do this instead:** Add the override to `css/custom.css` (loaded last, wins the cascade) or patch behaviour in `js/custom.js` (runs last). Example: the broken `<select>` arrow image in `base.css` is fixed via an inline-SVG override at `css/custom.css:83-89`, not by editing `base.css`.

### Calling Swiper autoplay stop/start to change marquee speed

**What happens:** To slow the services marquee, one might call `autoplay.stop()` / `start()`.
**Why it's wrong:** The theme config sets `disableOnInteraction:true`, so a stop→start pair is read as user interaction and permanently halts the marquee.
**Do this instead:** Only reassign `swiper.params.speed`; autoplay reads it each cycle. See the documented fix at `js/custom.js:113-146`.

### Assuming markup edits propagate across pages

**What happens:** Editing the nav or footer in one file and expecting it everywhere.
**Why it's wrong:** There is no include system; each of the 11 pages carries its own copy (verified: `site-header` and `site-footer` appear exactly once in every `*.html`).
**Do this instead:** Apply shared-chrome edits to all 11 HTML files in the same change.

## Error Handling

**Strategy:** Defensive guards in the custom JS layer; no global error reporting.

**Patterns:**
- Every `init*` in `js/custom.js` early-returns when its target element is absent (e.g. `if (!toggle || !nav) return;` at `js/custom.js:22`), so the same script is safe on all pages regardless of which elements exist.
- Idempotent DOM patches: a11y fixes check before writing (`if (!svg.getAttribute('aria-hidden'))` at `js/custom.js:155`) so repeated/late runs don't clobber state.
- Form validation surfaces user-facing messages via `.pfg-form-status` rather than throwing (`js/custom.js:82-88`).

## Cross-Cutting Concerns

**Logging:** None (no console logging in the custom layer; static site).
**Validation:** Client-side only — consent checkbox check in the lead form (`js/custom.js:81-88`); native HTML form attributes otherwise.
**Authentication:** None — fully public static site.
**Accessibility:** Treated as a cross-cutting concern handled in the custom layer — focus ring, `prefers-reduced-motion`, contrast tokens in `css/custom.css`; ARIA/name patches (`initSvgAria`, `initSearchA11y`, Swiper duplicate-H1 hiding) in `js/custom.js:148-200`.

---

*Architecture analysis: 2026-06-25*
