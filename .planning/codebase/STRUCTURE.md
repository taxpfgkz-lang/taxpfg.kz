# Codebase Structure

**Analysis Date:** 2026-06-25

## Directory Layout

```
taxpfg.kz/
├── index.html               # Homepage (hero slider, services marquee, blocks)
├── about.html               # О компании
├── services.html            # Услуги — overview / hub of all services
├── accounting.html          # Бухгалтерское сопровождение
├── accounting-recovery.html # Восстановление и наведение порядка в учёте
├── taxes.html               # Налоги и отчётность
├── consulting.html          # Консультации и помощь юриста
├── registration.html        # Регистрация и сопровождение бизнеса
├── contacts.html            # Контакты + lead form
├── privacy.html             # Политика конфиденциальности
├── 404.html                 # Страница ошибки
├── robots.txt               # Crawl directives
├── sitemap.xml              # XML sitemap
├── .gitignore
├── css/                     # All stylesheets (vendor theme + custom layer)
├── js/                      # All scripts (vendor libs + theme + custom layer)
├── fonts/                   # Icon webfonts (fontawesome, themify, pbmit icons)
├── images/                  # Theme + content imagery
└── .planning/               # GSD planning docs (this codebase map lives here)
```

## Directory Purposes

**Root (`./`):**
- Purpose: holds the 11 deliverable pages plus SEO/crawl files. Filename = URL path.
- Contains: `*.html`, `robots.txt`, `sitemap.xml`.
- Key files: `index.html` (entry), `contacts.html` (lead form).

**`css/`:**
- Purpose: all styling. Mix of vendor theme files (read-only) and the custom override layer.
- Contains: Bootstrap, plugin CSS, GudFin theme CSS, icon CSS, and the two custom-owned files.
- Key files: `css/base.css` (theme tokens/`:root` vars + Google-font `@import`s), `css/style.css` + `css/shortcode.css` (theme core), `css/responsive.css` (breakpoints), `css/custom.css` (custom override layer — edited).

**`js/`:**
- Purpose: all behaviour. Vendor libraries + theme init + custom layer.
- Contains: jQuery, GSAP (+ ScrollTrigger, SplitText), Swiper, AOS, Bootstrap, chart.js and other plugins; theme init; custom init.
- Key files: `js/scripts.js` (theme widget init), `js/gsap-animation.js` (GSAP/sticky header), `js/custom.js` (custom override layer — edited).

**`fonts/`:**
- Purpose: self-hosted icon webfonts referenced by the icon CSS.
- Contains: `.eot/.ttf/.woff/.woff2` for `fontawesome-webfont`, `themify`, `pbminfotech-base-icons`, `pbmit_gudfin`.
- Generated: yes (vendor). Committed: yes.

**`images/`:**
- Purpose: theme decorative assets + site content images.
- Contains: slider backgrounds (`slider1-0*.jpg`), patterns (`*pattarn*.png`), `og-image.jpg`, `fevicon.png`, process/service/team art, icon SVGs.
- Committed: yes.

**`.planning/`:**
- Purpose: GSD workflow artifacts. `codebase/` holds these architecture maps.
- Generated: partly (by GSD tooling). Committed: yes.

## Key File Locations

**Entry Points:**
- `index.html`: homepage; the only page with the hero Swiper slider and services marquee.

**Configuration:**
- `robots.txt`, `sitemap.xml`: SEO/crawler config.
- `.gitignore`: VCS ignore rules.
- No `package.json`, build config, or env files — none expected (static site).

**Core Logic / shared chrome:**
- Shared header markup: `<header class="site-header pbmit-header-style-1" id="masthead">` — duplicated in every page (e.g. `index.html:62`).
- Shared footer markup: `<footer class="site-footer pbmit-footer-style-1">` — duplicated in every page (e.g. `index.html:843`).
- Shared nav menu: `#site-navigation` with `ul.navigation` (e.g. `index.html:96-113`).
- Custom CSS layer: `css/custom.css`.
- Custom JS layer: `js/custom.js`.

**Asset load order (in every page `<head>` / end of `<body>`):**
- CSS: `index.html:30-54` (vendor → theme → `custom.css` last).
- JS: `index.html:1023-1057` (libs → `gsap-animation.js` → `scripts.js` → `custom.js` last).

## The 11 Page Files

| File | Purpose | Notes |
|------|---------|-------|
| `index.html` | Homepage | Hero slider, services marquee, CTA blocks, charts. Largest page (~73 KB). |
| `about.html` | О компании | Company story, values, process. |
| `services.html` | Услуги (hub) | Overview linking to the five service detail pages. |
| `accounting.html` | Бухгалтерское сопровождение | Service detail. |
| `accounting-recovery.html` | Восстановление учёта | Service detail. |
| `taxes.html` | Налоги и отчётность | Service detail. |
| `consulting.html` | Консультации и помощь юриста | Service detail. |
| `registration.html` | Регистрация и сопровождение бизнеса | Service detail. |
| `contacts.html` | Контакты | Hosts the `.pfg-form` lead form (→ WhatsApp). |
| `privacy.html` | Политика конфиденциальности | Legal/prose page. |
| `404.html` | Not-found page | Error page. |

All inner pages share a `pbmit-title-bar-wrapper` page-title/breadcrumb block (e.g. `about.html:165-170`) and use `.pfg-section` content sections.

## Key CSS Files

| File | Owner | Role |
|------|-------|------|
| `css/bootstrap.min.css` | vendor | Grid + base components |
| `css/fontawesome.css`, `css/themify-icons.css`, `css/pbminfotech-base-icons.css`, `css/pbmit_gudfin.css` | vendor | Icon fonts |
| `css/swiper.min.css`, `css/magnific-popup.css`, `css/aos.css` | vendor | Plugin styles (slider, lightbox, scroll-anim) |
| `css/shortcode.css` | theme | GudFin shortcode/component styles (largest) |
| `css/base.css` | theme | `:root` `--pbmit-*` tokens, typography, Google-font imports, header/search base |
| `css/style.css` | theme | Theme core layout |
| `css/responsive.css` | theme | Breakpoint rules |
| `css/custom.css` | **project** | Override/brand layer — edit here only |

## Key JS Files

| File | Owner | Role |
|------|-------|------|
| `js/jquery.min.js` | vendor | jQuery (theme depends on global `$`) |
| `js/popper.min.js`, `js/bootstrap.min.js` | vendor | Bootstrap behaviour |
| `js/swiper.min.js` | vendor | Sliders / marquee |
| `js/gsap.js`, `js/ScrollTrigger.js`, `js/SplitText.js` | vendor | GSAP animation stack |
| `js/aos.js` | vendor | Animate-on-scroll |
| `js/chart.js`, `js/circle-progress.js`, `js/numinate.min.js`, `js/jquery.countdown.min.js` | vendor | Counters / charts |
| `js/jquery.waypoints.min.js`, `js/jquery.appear.js`, `js/jquery.magnific-popup.min.js`, `js/theia-sticky-sidebar.js` | vendor | jQuery plugins |
| `js/gsap-animation.js` | theme | GSAP title animation + sticky header init |
| `js/scripts.js` | theme | Main theme init (sliders, AOS, counters, menu, charts) |
| `js/custom.js` | **project** | Override layer — edit here only |
| `js/email-decode.min.js` | vendor | Cloudflare email obfuscation helper |

## Naming Conventions

**Files:**
- Pages: lowercase, hyphenated, `.html` (e.g. `accounting-recovery.html`).
- Vendor/plugin assets keep upstream names (`jquery.min.js`, `swiper.min.css`).
- Custom-owned files are named `custom.*` (`css/custom.css`, `js/custom.js`).

**CSS classes — two namespaces:**
- `pbmit-*` = GudFin theme (vendor). Examples: `pbmit-header-style-1`, `pbmit-slider-area`, `pbmit-title-bar-wrapper`. Do not author new `pbmit-*` rules; only override.
- `pfg-*` = PrimeFinance Group (project). Examples: `pfg-section`, `pfg-card`, `pfg-grid`, `pfg-steps`, `pfg-form`, `pfg-logo`, `pfg-whatsapp-float`. Use this prefix for all new custom classes.

**CSS variables:**
- Theme tokens: `--pbmit-*` (e.g. `--pbmit-global-color: #ecab23` at `css/base.css:22`).
- Custom premium-layer tokens: `--pfg-*` (e.g. `--pfg-ink`, `--pfg-gold` at `css/custom.css:285-289`).

**JS:**
- Custom functions: `initX` camelCase inside a single IIFE (`js/custom.js`).
- Theme functions: `pbmit_*` snake_case (e.g. `pbmit_circle_progressbar` at `js/scripts.js:187`).

## Where to Add New Code

**New page:**
- Create `new-page.html` at repo root by copying an existing inner page (e.g. `about.html`) to inherit the shared `<head>`, header, footer, and script block.
- Add a link in the nav `ul.navigation` of **all 11 pages** (there is no shared include).
- Add the URL to `sitemap.xml`.

**New styling:**
- Append to `css/custom.css` only. Use `var(--pbmit-*)` theme tokens / `--pfg-*` custom tokens. Prefix new classes `pfg-`. Never edit `base.css`/`style.css`/`shortcode.css`/`responsive.css`.

**New behaviour:**
- Add an `initX()` function inside the IIFE in `js/custom.js` and call it from the `DOMContentLoaded` handler (`js/custom.js:6-13`). Early-return if the target element is missing so it stays safe on all pages. Avoid editing `scripts.js`/`gsap-animation.js`.

**New content section on a page:**
- Use `<section class="pfg-section">` (or `pfg-section pfg-section--alt` for the tinted variant) with `.pfg-card`/`.pfg-grid`/`.pfg-steps` inside, matching the pattern in `about.html:180-329`.

**Shared helpers:**
- CSS utilities: `css/custom.css` (`.pfg-muted`, `.pfg-lead`, `.pfg-prose`).
- JS: keep everything in the single `js/custom.js` IIFE (no module system).

## Special Directories

**`fonts/`:**
- Purpose: self-hosted icon webfonts. Generated vendor assets. Committed: yes.

**`.planning/`:**
- Purpose: GSD planning + this codebase map (`.planning/codebase/`). Committed: yes.

**`.git/`:**
- Standard VCS metadata. Not edited.

---

*Structure analysis: 2026-06-25*
