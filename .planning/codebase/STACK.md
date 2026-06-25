# Technology Stack

**Analysis Date:** 2026-06-25

## Languages

**Primary:**
- HTML5 - 11 static pages at repo root (`index.html`, `about.html`, `services.html`, `accounting.html`, `accounting-recovery.html`, `taxes.html`, `consulting.html`, `registration.html`, `contacts.html`, `privacy.html`, `404.html`)
- CSS3 - styling under `css/` (custom layer + vendored theme)
- JavaScript (ES5-style, browser, no modules) - behavior under `js/`

**Secondary:**
- JSON-LD - inline structured data (`schema.org` `AccountingService`) embedded in each page `<head>`, e.g. `index.html:24`
- XML - sitemap (`sitemap.xml`)

## Runtime

**Environment:**
- Browser only. This is a pure static website served directly as files. There is **NO server-side runtime**, no Node, no PHP, no backend process.

**Package Manager:**
- None. There is **no `package.json`**, no lockfile, no dependency manifest of any kind. All third-party libraries are vendored (committed) into `css/` and `js/`.

## Build System

**There is NO build system.** No bundler, transpiler, task runner, or compile step. Confirm points:
- No `package.json`, `webpack`, `vite`, `gulp`, `rollup`, or similar config anywhere.
- HTML pages reference assets directly by relative path (`css/...`, `js/...`).
- Vendored libraries are pre-minified files committed to the repo.
- Deployment = copy files to a static host. Editing = edit the file, refresh the browser.

The only "custom" (project-authored) layer added on top of the GudFin theme is:
- `css/custom.css` - PrimeFinance Group overrides (loaded last in `<head>`, e.g. `index.html:54`)
- `css/base.css` - base layer (theme-level, loaded before `style.css`)
- `js/custom.js` - project behavior: mobile menu, lead form → WhatsApp, marquee tuning

Everything else under `css/` and `js/` is vendor/theme code and should be treated as read-only.

## Frameworks & Vendored Libraries

Versions below are read directly from each file's banner/header.

**CSS frameworks / theme:**
- Bootstrap `5.2.0-beta1` - `css/bootstrap.min.css` + `js/bootstrap.min.js` (grid, layout, components)
- GudFin HTML theme - `css/style.css`, `css/base.css`, `css/responsive.css`, `css/shortcode.css`, `css/pbmit_gudfin.css` (PBMIT/Pbminfotech commercial theme this site is based on)

**JavaScript libraries (in `js/`, load order per `index.html:1023-1057`):**
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

**Project-authored JS:**
- `js/custom.js` - the only hand-written script. Loaded last (`index.html:1057`).

## Icon Fonts

Self-hosted icon webfonts under `fonts/` with matching CSS:
- Font Awesome - `fonts/fontawesome-webfont.{eot,ttf,woff,woff2}` via `css/fontawesome.css`
- Themify Icons - `fonts/themify.{eot,ttf,woff}` via `css/themify-icons.css`
- Pbminfotech base icons - `fonts/pbminfotech-base-icons.{eot,ttf,woff,woff2}` via `css/pbminfotech-base-icons.css`
- Pbmit GudFin icons - `fonts/pbmit_gudfin.{eot,ttf,woff,woff2}` via `css/pbmit_gudfin.css`

## Text Fonts

Loaded remotely from Google Fonts via `@import` in `css/base.css:16-19`:
- Be Vietnam Pro - body text (`--pbmit-body-typography-font-family`)
- Plus Jakarta Sans - headings and buttons
- Roboto - imported (theme default)
- Montserrat - referenced as a fallback family in `css/base.css:272` (not explicitly imported)

Note: text fonts are an **external runtime dependency** on `fonts.googleapis.com` (see INTEGRATIONS.md).

## Configuration Files

- `robots.txt` - allows all crawlers, points to sitemap (`Sitemap: https://taxpfg.kz/sitemap.xml`)
- `sitemap.xml` - 10 URLs with `lastmod` 2026-06-20, `changefreq` monthly, priorities 0.3–1.0 (`accounting-recovery.html` and `404.html` are not listed)
- `.gitignore` - ignores `node_modules/`, OS junk, logs, Playwright/screenshot audit artifacts, root-level images, and Python bytecode
- Favicon: `images/fevicon.png` referenced via `<link rel="shortcut icon">` (`index.html:26`)

No `tsconfig.json`, `.eslintrc`, `.prettierrc`, `.nvmrc`, or any tooling config exists — consistent with the no-build-system nature of the project.

## Platform Requirements

**Development:**
- Any text editor plus a browser. Optionally a static file server (e.g. `python -m http.server`) so relative paths and the Google Fonts/Maps requests resolve over HTTP.

**Production:**
- Any static host / CDN capable of serving plain files (the canonical/OpenGraph URLs and sitemap target `https://taxpfg.kz/`). No application server, database, or runtime environment required.

---

*Stack analysis: 2026-06-25*
