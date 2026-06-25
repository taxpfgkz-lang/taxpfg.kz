# Testing Patterns

**Analysis Date:** 2026-06-25

## Test Framework

**There is no automated test framework in this project.**

This is a static HTML website with no build system, no `package.json`, no test runner, no CI pipeline, and no backend. There are no unit tests, integration tests, snapshot tests, or end-to-end test files anywhere in the repository. Searching for `*.test.*` / `*.spec.*` / `jest.config` / `vitest.config` / `playwright.config` returns nothing — none exist.

Do **not** attempt to "set up the standard test framework for the ecosystem." For a hand-authored static HTML/CSS/JS site with three custom source files (`css/custom.css`, `css/base.css`, `js/custom.js`) layered over a purchased theme, a unit-test harness adds no value. Quality is enforced through the manual UI/UX + accessibility audit process described below.

## Actual QA Approach

Quality assurance is **manual, browser-based, and accessibility-driven**, performed via Playwright automation plus Chrome DevTools / Lighthouse. The git history is effectively the test log — each audit pass produced a dated `feat`/`fix` commit and a corresponding numbered "Этап" (stage) section in `css/custom.css`.

**Tooling used:**
- **Playwright** (MCP / browser automation) — drives a real browser to measure the actual rendered DOM (computed styles, element box sizes, scroll width) rather than trusting what the CSS file *says*. Project memory notes the key lesson: *"верить DOM-измерению, а не тексту CSS"* (trust the DOM measurement, not the CSS text). For example, the section-spacing audit (`css/custom.css:628-645`, Этап 13) records measured `padding-top`/`padding-bottom` per section across breakpoints.
- **Chrome DevTools + Lighthouse** — accessibility, contrast, and "Agentic Browsing" scoring. Multiple commits cite Lighthouse results (e.g. `370220c` "Lighthouse Agentic Browsing 50→100", `css/custom.css:113` "Lighthouse-аудит").
- **axe** (via the a11y tooling) — referenced for specific WCAG rule IDs in CSS comments (`link-in-text-block`, contrast ratios), e.g. `css/custom.css:260-267`.

**What the audits check** (the de-facto test checklist):
- **Responsive layout** at fixed breakpoints. The audits exercise desktop / tablet / mobile widths explicitly: **1440 / 1024 / 768 / 390 / 360** (see `css/custom.css:521-528`, Этап 10) and a reduced set **1440 / 768 / 390** for the spacing audit (`css/custom.css:630`). Checks: no horizontal scroll on any page at any width, no clipped headings, consistent section rhythm.
- **Accessibility, targeting 0 violations.** Contrast (WCAG AA ≥4.5:1 text, ≥3:1 large), tap-target size (WCAG 2.5.5 / 2.5.8, ≥44px), single semantic `<h1>` per page, accessible names for icon controls and search field, `aria-hidden` on decorative SVGs, `prefers-reduced-motion` respected. Each fix comment cites the specific WCAG criterion.
- **Visual / "premium" polish** — typography line length (measure ~60–75 cpl), letter-spacing for Cyrillic, button/card tactility, overlay readability on hero/title-bar photos.
- **Cross-page coverage:** all **11 pages** are swept each audit pass (`404.html`, `about.html`, `accounting-recovery.html`, `accounting.html`, `consulting.html`, `contacts.html`, `index.html`, `privacy.html`, `registration.html`, `services.html`, `taxes.html`).

**Run commands:**
```bash
# No test commands exist. There is nothing to `npm test` / `npm run build`.
```

## Known QA Tooling Caveat

Per project memory (`workflow-api-proxy-balance.md`): the multi-agent Workflow API proxy has been failing (HTTP 400, no balance), so automated audit sub-agents cannot be relied on. **Critical checks must be duplicated manually via Playwright**, and DOM measurement is trusted over CSS-file text. Budget for hands-on verification rather than assuming an automated agent covered it.

## How to Verify a Change

Since there is no test command, verification is done by observing the change in a browser:

1. **Open the page directly.** The site is fully static — open any `*.html` file in a browser (`file://`) or serve the folder over a simple static server and load the page. No build step is required; edits to `css/custom.css` / `js/custom.js` take effect on reload.
   ```bash
   # optional local static server (any will do)
   python -m http.server 8000
   # then open http://localhost:8000/index.html
   ```
2. **Drive it with Playwright** to reproduce the audit conditions:
   - Load each affected page at the standard breakpoints (1440 / 768 / 390 at minimum).
   - Measure the **rendered DOM**, not the CSS source: computed styles, `getBoundingClientRect` sizes for tap targets, `document.documentElement.scrollWidth` vs viewport for horizontal-scroll checks.
   - Run the accessibility audit (axe / Lighthouse) and confirm **0 violations** for the area you touched — or, if a violation is a known accepted theme limitation, confirm it matches one already documented (e.g. the mobile search tap-target at `css/custom.css:141-151`).
3. **Manually exercise the JS behaviors** in `js/custom.js`, since they have no automated coverage:
   - Mobile menu open/close (hamburger tap, backdrop click, Escape key, link click).
   - Floating WhatsApp button appears and links to the right number.
   - `.pfg-form` submit: blocks without consent, otherwise opens `wa.me` with the assembled Russian message and shows the status line.
   - Marquee runs at the slowed speed and keeps scrolling.
   - With OS "reduce motion" enabled, the hero slider and marquee still animate (brand identity preserved) while card/button micro-interactions are stilled.
4. **Confirm load order** is intact after any markup edit: vendor CSS before `custom.css`, vendor JS before `custom.js` (see `CONVENTIONS.md`).

## Test Types

- **Unit Tests:** None. Not applicable to this project.
- **Integration Tests:** None.
- **E2E / Visual / A11y:** Manual, via Playwright + Chrome DevTools/Lighthouse/axe, as described above. This is the only "test suite" the project has.

## Coverage

No coverage tooling exists or applies. The de-facto coverage target is **all 11 pages at the standard breakpoints with 0 new accessibility violations** per audit pass. Audit findings and their fixes are recorded as dated stage blocks in `css/custom.css` and in `docs/` audit notes referenced by those comments (e.g. `docs/UI-AUDIT-2026-06-23.md` cited at `css/custom.css:150`).

---

*Testing analysis: 2026-06-25*
