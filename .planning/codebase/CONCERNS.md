# Codebase Concerns

**Analysis Date:** 2026-06-25

## Tech Debt

**Duplicated header/footer markup across 11 HTML pages (no templating):**
- Issue: This is a static site with no build step or templating engine. The full site header (logo, top-bar, nav menu, search, off-canvas mobile menu) and the footer are hand-copied into every page. `site-header`/`pbmit-header` markup appears 8–9 times per file across all 11 pages; `<footer>` once per page. Any change to a nav link, phone number, address, or footer copyright must be edited 11 times by hand.
- Files: `index.html`, `about.html`, `services.html`, `accounting.html`, `accounting-recovery.html`, `consulting.html`, `taxes.html`, `registration.html`, `contacts.html`, `privacy.html`, `404.html`
- Impact: High drift risk. A header edit applied to 10 of 11 pages leaves one stale and there is no automated check to catch it. The same applies to the 18 `<script>` tags and 13 `<link rel="stylesheet">` tags repeated verbatim in every `<head>`.
- Fix approach: Introduce a minimal static-site generator or HTML include mechanism. Options that fit a no-backend host: a build step (Eleventy/Nunjucks, Astro, or a tiny Node/Handlebars script) that compiles partials → 11 pages; or, if the build pipeline must stay zero-config, client-side HTML includes (fetch + `<template>`) — though that hurts SEO and adds a flash of unstyled content, so a build step is preferred. Until then, treat header/footer/`<head>` as a "change-all-11" checklist item.

**No build, minification, or bundling pipeline:**
- Issue: There is no `package.json`, bundler, or task runner. Assets are served as-is. Several files are large and unminified despite their names, and the page loads ~18 separate JS requests + ~13 CSS requests with no concatenation or tree-shaking.
- Files: entire `js/` and `css/` directories; project root (no `package.json`, no config)
- Impact: Larger payloads, more HTTP round-trips, and no opportunity to drop dead code (see chart.js below). No cache-busting hashes either, so updates to `css/custom.css` risk being served stale from CDN/browser cache.
- Fix approach: Add a lightweight build (esbuild/Vite or even a script) to minify+bundle vendor JS/CSS, fingerprint filenames, and emit the 11 pages from partials. This pairs naturally with the templating fix above.

## Known Bugs

**Header search target-size overlap (a11y, WCAG 2.2 AA 2.5.8) — intentionally unfixed:**
- Symptoms: On mobile (≤1200px) the theme's absolutely-positioned hamburger toggle (`.nav-menu-toggle`, `position: absolute; right: 0`) visually overlaps the search icon by ~16px, leaving a clean tap zone < 24px. Lighthouse mobile flags target-size.
- Files: documented inline at `css/custom.css:141-151`; the custom layer adds a 44×44 hit-zone at `css/custom.css:152-159` but cannot resolve the overlap without rewriting the vendor toggle layout.
- Trigger: Mobile viewport, tap between hamburger and search glyph.
- Workaround: Left as a known limitation per project decision (Этап 10). Desktop scores 100. Fixing it requires rewriting the vendor off-canvas absolute layout — a high-risk zone deliberately avoided. Tracked in `docs/UI-AUDIT-2026-06-23.md` (referenced from the CSS comment; note the docs/ folder was largely deleted in the working tree per git status, so verify this reference still resolves).

## Security Considerations

**Third-party assets fully vendored, no SRI / no CSP:**
- Risk: All JS/CSS is self-hosted (good — no external CDN supply-chain exposure at runtime), but there is no Content-Security-Policy and the many inline `style="..."` attributes (10 in `index.html`, 10 in `404.html`, 4–5 elsewhere) plus inline `<script type="application/ld+json">` would force `style-src 'unsafe-inline'` if a CSP were added later.
- Files: `index.html`, `404.html`, all pages (inline styles); `<head>` JSON-LD blocks
- Current mitigation: Static site, no user input processing server-side, no forms posting to a backend (verify form action targets before launch).
- Recommendations: Add security headers at the host level (CSP, X-Content-Type-Options, Referrer-Policy). Migrate inline styles into `css/custom.css` to allow a stricter `style-src`.

## Performance Bottlenecks

**chart.js loaded into the repo but never used:**
- Problem: `js/chart.js` is 208 KB (the single largest JS file) and is **not referenced by any HTML page** (`grep "chart.js" *.html` → no match). It is dead weight in the repo. (Note: it is not in the 18 script tags, so it is not actually shipped to the browser — but it bloats the repo and invites confusion.)
- Files: `js/chart.js`
- Cause: Inherited from the GudFin theme; the chart demo widget was never used on this site.
- Improvement path: Delete `js/chart.js`. Audit the other 18 loaded scripts the same way — `js/jquery.countdown.min.js` (5 KB) and `js/circle-progress.js` (15 KB) are loaded on all 11 pages; countdown has no visible invocation in `js/scripts.js`/`js/custom.js`, and circle-progress is only invoked defensively (`if typeof $.fn.circleProgress === "function"`). Drop any widget not present on a given page.

**Heavy unminified CSS/JS payload shipped site-wide:**
- Problem: Every page loads the full vendor stack regardless of what it uses. Notable sizes:
  - CSS: `bootstrap.min.css` 193 KB, `shortcode.css` 195 KB, `responsive.css` 103 KB, `style.css` 70 KB, `fontawesome.css` 36 KB, `aos.css` 26 KB → ~760 KB CSS total across 13 files.
  - JS: `swiper.min.js` 135 KB, `jquery.min.js` 87 KB, `gsap.js` 65 KB (unminified despite no `.min`), `bootstrap.min.js` 60 KB, `ScrollTrigger.js` 38 KB → ~600 KB JS shipped per page (excluding the unused chart.js).
  - Misleadingly named: `swiper.min.js` (135 KB) and `bootstrap.min.css` (193 KB) carry `.min` but are large; `gsap.js`, `ScrollTrigger.js`, `SplitText.js`, `chart.js`, `aos.js`, `circle-progress.js` are unminified.
- Files: `css/`, `js/` directories
- Cause: Theme ships everything; no build step to subset, minify, or split per-page.
- Improvement path: Minify all assets, subset FontAwesome to used glyphs, split CSS so pages only load what they use, and lazy-load GSAP/Swiper only where animations/sliders exist. A build step (above) enables all of this.

**Unoptimized images (~6.9 MB, no WebP/AVIF):**
- Problem: `images/` is ~6.9 MB across 43 files, all PNG/JPG/SVG (0 WebP/AVIF). Largest: `images/video-bg.png` 1.18 MB, `images/service-left-bg.png` 693 KB, `images/pattarn-01.png` 518 KB, `images/fontawesome-webfont.svg` 442 KB, `images/processbox-img-04.png` 331 KB, plus three slider JPGs ~260–304 KB each.
- Files: `images/video-bg.png`, `images/service-left-bg.png`, `images/pattarn-01.png`, `images/processbox-img-*.png`, `images/slider1-0*.jpg`
- Cause: Raw theme/demo assets, no compression pass.
- Improvement path: Convert large PNG backgrounds and slider photos to WebP/AVIF with `<picture>` fallbacks, compress, and add explicit `width`/`height` + `loading="lazy"` on below-fold images.

## Fragile Areas

**CSS specificity wars between GudFin theme and the custom override layer:**
- Files: `css/custom.css` (951 lines, 52 KB), `css/base.css` (1166 lines), competing with `css/style.css`, `css/shortcode.css`, `css/responsive.css`, `css/bootstrap.min.css`
- Why fragile: `css/custom.css` uses `!important` 59 times and `css/base.css` 9 times to win against the deeply-nested theme selectors. `custom.css` and `base.css` load last (after `style.css`/`responsive.css`), so order is doing real work. Any reordering of the `<link>` tags, or a theme selector change, can silently break overrides. The premium "ink + gold" layer is built entirely on top of vendor CSS it does not control.
- Safe modification: Always keep `custom.css` and `base.css` last in the `<head>`. Prefer increasing selector specificity over adding more `!important`. When an override fights the theme, inspect the exact winning vendor rule rather than escalating to `!important`.
- Test coverage: None (no visual regression tests) — see below.

**Dependency on theme vendor files that cannot be easily updated:**
- Files: `js/scripts.js`, `js/gsap-animation.js`, `css/style.css`, `css/shortcode.css`, `css/responsive.css`, `css/pbmit_gudfin.css`, `css/pbminfotech-base-icons.css`
- Why fragile: The site is pinned to a downloaded snapshot of the GudFin theme (vendor files dated июн 18). There is no version manifest, no upstream link, and the custom layer monkey-patches theme behavior (e.g., defensive `circleProgress` checks in `js/scripts.js`, `pbmit-*` class overrides in `custom.css`). Pulling a newer theme version would require re-applying every custom override by hand and re-auditing a11y.
- Safe modification: Treat vendor files as read-only. Put all changes in `css/custom.css`, `css/base.css`, and `js/custom.js`. Document any unavoidable vendor edit prominently.
- Test coverage: None.

## Test Coverage Gaps

**No automated tests of any kind:**
- What's not tested: No unit, integration, visual-regression, link-checker, HTML-validation, or accessibility-automation tests exist. There is no test runner, CI config, or `package.json` to hang tests on.
- Files: entire repo
- Risk: The "edit header/footer in 11 places" workflow has no safety net — a broken nav link, a stale phone number on one page, a malformed `<head>`, or a regressed a11y fix can ship unnoticed. CSS override breakage (above) is invisible without a human eyeballing every page at every breakpoint.
- Priority: High. Cheap wins available even without a backend: an HTML validator + broken-link checker (e.g., `html-validate`, `linkinator`) and Lighthouse/axe CI runs across all 11 pages. Pair with Playwright visual-regression snapshots to guard the custom CSS layer against vendor/order regressions.

## SEO / Meta Consistency

**Per-page meta is consistent and mostly complete — keep it that way:**
- State: All 11 pages have exactly 1 `<title>`, 1 `meta description`, 1 `rel=canonical`, OG + Twitter image tags, and JSON-LD (`index.html` and `404.html` carry 1 JSON-LD block, content pages carry 2). Titles and descriptions are unique per page (verified). `<html lang="ru">` is set.
- Files: all `*.html` `<head>` sections
- Risk: Because every `<head>` is hand-maintained per page (no templating), this consistency is fragile — adding a 12th page or editing OG tags means manually replicating the full pattern, and there is no test to confirm canonical/OG/JSON-LD stay correct and unique.
- Recommendation: Fold `<head>` generation into the same templating/build fix so per-page meta is data-driven (title/description/canonical as front-matter) rather than copy-pasted. Add a build-time check that every page has a unique title + canonical.

---

*Concerns audit: 2026-06-25*
