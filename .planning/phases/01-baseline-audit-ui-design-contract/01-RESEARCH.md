# Phase 1: Baseline Audit + UI Design Contract - Research

**Researched:** 2026-06-26
**Domain:** Static no-build site audit tooling + design-contract groundwork (documents, not code)
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Phase produces DOCUMENTS, not code.** No changes to `custom.css`/`base.css`/`custom.js` in this phase — only `.planning/` artifacts.
- Baseline снимается двумя инструментами: **Lighthouse + axe-core** (Playwright-axe / axe DevTools) по всем **11 страницам**.
- Визуальный аудит на **5 viewport-ах: 1440 / 1024 / 768 / 390 / 360**, измерения DOM-measured через Playwright (верить измерению DOM, а не тексту CSS).
- Baseline-числа фиксируются таблицей per-page: a11y score, perf, CLS, LCP.
- Проблемы группируются **по типам блоков** (header/footer/hero/cards/forms — общие на всех 11), а не постранично.
- Spacing scale: 4px-база (4/8/12/16/24/32/48/64/96) как токены `--pfg-space-*`.
- Type scale: `clamp()` fluid, ratio ≈1.25, base body 16–18px.
- Цветовые токены фиксируются как есть (ink `#16222d`, ink-deep `#0f1820`, gold `#ecab23`, gold-deep `#d6960f`, gold-ink `#7a560a`). Палитра НЕ расширяется.
- Контраст-флор WCAG AA: текст ≥4.5:1, крупный/UI ≥3:1; золото как body-текст запрещено.
- Обязательные состояния всех интерактивных элементов: hover / focus-visible / active / disabled; focus всегда видим.
- Иерархия кнопок: primary / secondary / ghost.
- Артефакты — отдельные секции/файлы под `.planning/phases/01-*/`: AUDIT, CONFLICT-CATALOG, DESIGN-CONTRACT, IMPL-PLAN.
- Каталог конфликтов: `!important` (~59 baseline) + do-not-touch классы (`swiper-*`, `data-aos*`, `pbmit-*`) с привязкой к файлу/строке.
- Hard-constraints в контракте явно: visual-only, vendor read-only, no `@layer`, focus-always, scoped-motion.
- Открытые вопросы research решаются в этой фазе (font-loading, img-инвентарь, pricing/FAQ/modal, судьба chart.js).

### Claude's Discretion
- Точный формат таблиц и внутренняя нумерация секций в артефактах.
- Какие именно страницы выбрать как репрезентативные при группировке проблем по типам блоков.

### Deferred Ideas (OUT OF SCOPE)
- PERF-01/02/03 (WebP/AVIF, удаление chart.js 208 КБ, font-display/preload) — v2, отдельный milestone.
- MNT-01 (шаблонизация header/footer) — потребовал бы build-систему, вне no-build.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUD-01 | Снять baseline (Lighthouse + axe-core, a11y/perf/CLS) по всем 11 страницам ДО правок | Tooling path resolved (Q6): npx Lighthouse 13.4.0 + `@axe-core/playwright` 4.12.1 against `python -m http.server`. Chrome present. |
| AUD-02 | UI audit report — визуальные проблемы что/где/почему, desktop/tablet/mobile | Block-type taxonomy resolved: 10/11 pages share title-bar; index.html is the only non-titlebar page; header/footer/form identical ×11. |
| AUD-03 | Каталог конфликтов `custom.css` ↔ vendor + список `!important` (~59) и do-not-touch классов | `!important` count **verified = 59** (Q5). do-not-touch namespaces enumerated. |
| AUD-04 | UI design contract — токены, scales, цвет+контраст, состояния, hard-constraints | Already drafted/approved in 01-UI-SPEC.md; research confirms font-loading + component reality feeding it. |
| AUD-05 | Implementation plan — какие файлы менять, зачем, порядок | Component-to-file map + img inventory + absent-blocks (no pricing, no FAQ, no live modal) scope later phases. |
</phase_requirements>

## Summary

This is a **documentation phase** for a frozen, no-build static site (11 HTML pages on the GudFin/PBMIT theme + Bootstrap 5.2 + a thin `pfg-*` override layer). No code changes. The research goal was to resolve the open factual questions that feed the AUDIT, CONFLICT-CATALOG, DESIGN-CONTRACT, and IMPL-PLAN artifacts — and all six are now resolved against the real files.

Key factual findings: fonts load via **`@import` inside `css/base.css` (lines 16–19)**, not via `<head>` `<link>` — there is no preconnect/preload (relevant to v2 perf, out of scope now). The site has **no pricing block, no FAQ accordion, and no instantiated modal anywhere** — Magnific Popup is loaded on all 11 pages but its trigger selectors (`.pbmin-lightbox-video`, `a.pbmit-lightbox`) appear in zero markup, so CMP-05 and CMP-06 reduce to "feature absent — document and descope." chart.js is **not referenced by any page** and stays out of scope. The `!important` count in `custom.css` is **exactly 59**, matching the ROADMAP estimate.

For the baseline (AUD-01), the machine has Node 24.11.1, npm 11.16.0, Python 3.14.0, and Chrome installed. The practical path is a local static server (`python -m http.server`) plus npx-invoked Lighthouse 13.4.0 and `@axe-core/playwright` 4.12.1 driven through the existing Playwright MCP — all external tools, no project build introduced.

**Primary recommendation:** Plan the phase as four document-producing waves (baseline capture → visual audit by block-type → conflict catalog → contract+impl-plan). Use the resolved facts below verbatim; do not re-investigate. Treat CMP-05/CMP-06/CNV-02 as "absent on current site" and have the planner mark them descoped-or-net-new for later phases rather than "audit existing."

## Architectural Responsibility Map

This phase changes no code; the "tier" here is which artifact owns each finding.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Lighthouse/axe baseline numbers | AUDIT artifact | — | Regression floor (AUD-01); per-page table |
| Visual problem enumeration | AUDIT artifact | DESIGN-CONTRACT | Grouped by block-type, fed by DOM-measured Playwright |
| `!important` / do-not-touch ledger | CONFLICT-CATALOG | — | Vendor-override accounting (AUD-03) |
| Token / scale / color / state rules | DESIGN-CONTRACT (01-UI-SPEC.md) | — | Already drafted+approved; AUD-04 |
| File-change order for Phases 2–5 | IMPL-PLAN | — | AUD-05; consumes component-to-file map below |

## Standard Stack

No application stack is chosen — the site is frozen and vendor-read-only. The "stack" here is **external audit tooling**, run without touching the project (no `package.json`, no install into repo). Invoke via `npx` so nothing is added to the no-build site.

### Core (audit tooling — external, npx-invoked)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| lighthouse | 13.4.0 | Per-page perf / a11y / CLS / LCP baseline | Reference Chrome auditing tool; CLI emits JSON+HTML [VERIFIED: npm registry] |
| @axe-core/playwright | 4.12.1 | Programmatic WCAG rule checks inside Playwright runs | Deque axe is the industry a11y engine; integrates with existing Playwright MCP [VERIFIED: npm registry] |
| playwright | 1.61.1 | DOM-measured viewport audit @ 1440/1024/768/390/360 + screenshots | Already the project's verify channel (memory: trust DOM over CSS text) [VERIFIED: npm registry] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @axe-core/cli | 4.12.1 | CLI-only axe scan if Playwright route is unavailable | Fallback for quick per-URL a11y scan [VERIFIED: npm registry] |
| Python http.server | stdlib (Py 3.14.0) | Serve 11 HTML over HTTP so relative paths + Google Fonts/Maps resolve | Built-in; `python -m http.server 8080` [VERIFIED: local probe] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Python http.server | `npx http-server` / `npx serve` | Equivalent; Python is already installed, one less npx download |
| Lighthouse CLI | Chrome DevTools Lighthouse panel (manual) | Manual is fine for spot-checks but not reproducible across 11 pages; CLI emits storable JSON for the floor |
| @axe-core/playwright | axe DevTools browser extension | Extension is manual/not scriptable; Playwright integration scales to 11 pages |

**Installation:** No install into the repo. Run tools ephemerally:
```bash
# Serve the site (from repo root)
python -m http.server 8080

# Lighthouse per page (repeat per URL), JSON+HTML output
npx -y lighthouse@13.4.0 http://localhost:8080/index.html \
  --output=json --output=html --output-path=./.planning/phases/01-baseline-audit-ui-design-contract/baseline/index \
  --chrome-flags="--headless=new" --only-categories=performance,accessibility

# axe via the existing Playwright MCP (preferred) or @axe-core/playwright in an ephemeral script
```
Audit artifacts land under `.planning/` (the repo `.gitignore` already excludes Playwright/screenshot audit artifacts at root — confirm baseline JSON path is intentionally kept or ignored).

**Version verification:** `npm view` run 2026-06-26 — lighthouse 13.4.0, @axe-core/playwright 4.12.1, @axe-core/cli 4.12.1, playwright 1.61.1. Local: node v24.11.1, npm 11.16.0, python 3.14.0, Chrome present at `C:\Program Files\Google\Chrome\Application\chrome.exe`.

## Package Legitimacy Audit

> This phase installs **nothing** into the project (no-build, no `package.json`). Tools below are external, npx-invoked, ephemeral. Listed for the planner because they are still external dependencies the baseline relies on.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| lighthouse | npm | ~8 yrs | millions/wk | github.com/GoogleChrome/lighthouse | OK | Approved (npx, ephemeral) |
| @axe-core/playwright | npm | est. several yrs | high | github.com/dequelabs/axe-core-npm | OK | Approved (npx, ephemeral) |
| @axe-core/cli | npm | est. several yrs | high | github.com/dequelabs/axe-core-npm | OK | Approved (fallback) |
| playwright | npm | several yrs | millions/wk | github.com/microsoft/playwright | OK | Approved (already project verify channel) |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

*All four are first-party Google/Microsoft/Deque tooling with well-known repos. Verdicts above are based on registry existence + known-publisher reputation; no automated legitimacy seam was run because nothing is installed into the project tree. If the planner adds an install step, run `package-legitimacy check` first.*

## Architecture Patterns

### System Architecture Diagram (audit data flow)

```
11 HTML files (repo root)
        │  served over HTTP
        ▼
python -m http.server 8080  ──► relative css/js + Google Fonts(@import) + Maps iframe resolve
        │
        ├──► Lighthouse CLI (headless Chrome) ──► per-page JSON/HTML ──► AUDIT table (perf/a11y/CLS/LCP)
        │
        ├──► Playwright MCP @ 5 viewports ──► DOM measurements + screenshots ──► AUDIT (visual problems by block-type)
        │
        └──► @axe-core/playwright ──► WCAG rule violations ──► AUDIT (a11y findings) + DESIGN-CONTRACT (contrast floor)

Static analysis (no server):
  grep custom.css ──► !important ledger (=59) + do-not-touch namespaces ──► CONFLICT-CATALOG
  HTML/CSS read ──► component-to-file map + img inventory ──► IMPL-PLAN
```

File-to-artifact mapping lives in the Architectural Responsibility Map above; the diagram shows data flow.

### Recommended Artifact Structure
```
.planning/phases/01-baseline-audit-ui-design-contract/
├── 01-RESEARCH.md            # this file
├── 01-CONTEXT.md             # locked decisions
├── 01-UI-SPEC.md             # DESIGN-CONTRACT (AUD-04, approved)
├── 01-AUDIT.md               # AUD-01 baseline table + AUD-02 visual problems
├── 01-CONFLICT-CATALOG.md    # AUD-03 !important ledger + do-not-touch
├── 01-IMPL-PLAN.md           # AUD-05 file-change order for Phases 2–5
└── baseline/                 # Lighthouse JSON/HTML + Playwright screenshots
```

### Pattern 1: Block-type grouping over per-page enumeration
**What:** Audit the shared chrome once (header, footer, nav, form, title-bar) and note page-specific deltas, rather than repeating identical findings 11×.
**When to use:** Any finding on duplicated markup.
**Evidence:** Header/footer/nav/script block is copy-pasted into all 11 files; `pbmit-title-bar-wrapper` present on 10/11 (all except `index.html`); the lead form (`.pfg-form`) is the contacts-page form. [VERIFIED: grep across *.html]

### Pattern 2: DOM-measured truth
**What:** Record values measured from the live DOM via Playwright, not values read from CSS source text.
**When to use:** Every visual/spacing/contrast finding.
**Rationale:** Project memory `workflow-api-proxy-balance.md` — vendor cascade + media queries make CSS source text unreliable; trust the rendered box.

### Anti-Patterns to Avoid
- **Auditing absent features as if present:** Do not write "FAQ accordion has poor ARIA" — there is no accordion. Record absence, descope to later phase as net-new if desired.
- **Per-page duplication:** 11× the same header finding inflates the report and obscures real per-page deltas.
- **Trusting CSS text:** A rule in `custom.css` may be overridden by a vendor media query; measure the DOM.
- **Introducing a build to run audits:** Audit tools are external/npx — never add `package.json` or a bundler to the site.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Contrast-ratio checking | Custom WCAG math over computed colors | axe-core (`@axe-core/playwright`) | axe handles compositing, opacity, gradients, text-size thresholds correctly |
| Perf/CLS/LCP measurement | Manual timing scripts | Lighthouse CLI | Reproducible, stores JSON floor, standard metric definitions |
| Cross-viewport measurement | Manual resize + eyeball | Playwright @ fixed viewports | Deterministic DOM box measurement at 1440/1024/768/390/360 |
| Local HTTPS-ish serving | Custom Node server | `python -m http.server` | Already installed; resolves relative paths + remote fonts/maps |

**Key insight:** This phase's "implementation" is measurement and documentation. The hand-roll risk is reimplementing audit math that mature tools already get right — and the no-build constraint means those tools must stay external.

## Resolved Open Questions (the core deliverable of this research)

### Q1 — Live `<head>` font-loading config — RESOLVED
Fonts are **NOT** loaded via `<head>` `<link>`. No `<link rel="preconnect">`, no `preload`, no Google Fonts `<link>` exists in any HTML head. [VERIFIED: grep *.html — zero matches for googleapis/gstatic/preconnect/preload]

Fonts load via **`@import` at the top of `css/base.css`** (a vendor file): [VERIFIED: css/base.css:16-19]
```css
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:...&display=swap');   /* base.css:16 — duplicated at :18 */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap'); /* :17 */
@import url('https://fonts.googleapis.com/css2?family=Roboto:...&display=swap');            /* :19 */
```
Notes for later (v2 / PERF-03 — out of scope now): (a) `display=swap` is already present on all imports; (b) Be Vietnam Pro is imported **twice** (lines 16 and 18 — duplicate); (c) `@import` blocks rendering and chains after CSS download (worst-case for FOUT/CLS) — but base.css is vendor read-only, so any perf fix would need a `<head>` `<link preload>` added across 11 files, which is explicitly v2. Font families consumed via tokens: body `"Be Vietnam Pro"` (`base.css:35`), headings/buttons `"Plus Jakarta Sans"` (`base.css:41,45`); `"Roboto"` and `"Montserrat"` referenced as theme fallbacks (`base.css:272`, `style.css:835`).

### Q2 — `<img>` vs CSS-background inventory — RESOLVED (coarse)
[VERIFIED: grep *.html + ls images/]

`<img>` tags total **12**, on only 2 pages:
- `index.html`: 11 `<img>` — `about-01.jpg`, `about-02.png`, `infobox-img.png`, `service-left-img.png`, `static-box-0{1,2,3}.jpg`, `processbox-img-0{1,2,3,4}.png`. All carry `loading="lazy" decoding="async"`.
- `services.html`: 1 `<img>` — `service-left-img.png`.

CSS-background images (the dominant pattern):
- **Inline `style="background-image:url(...)"`** in `index.html` only: 3 hero slides (`slider1-0{1,2,3}.jpg`) + 3 static boxes (`static-box-0{1,2,3}.jpg`). [VERIFIED: index.html]
- **Title-bar background** on all 10 inner pages via vendor CSS: `shortcode.css:4924 background-image:url(../images/titlebar-img.jpg)` applied to `.pbmit-title-bar-wrapper` (present on 10/11 pages). [VERIFIED: css/shortcode.css:4922-4924 + grep]
- **Decorative pattern PNGs** (`pattarn-*.png`, `*-bg-pattarn.png`, `service-bg.png`, `video-bg.png`, etc.) referenced from vendor CSS as section backgrounds.

Logo is **text, not an image**: `.pfg-logo` span (`index.html:71-72`), so no logo asset to audit.

Asset store: `images/` ≈ **6.9 MB total**. Heaviest: `video-bg.png` 1.18 MB, `service-left-bg.png` 693 KB, `pattarn-01.png` 517 KB, four `processbox-img-*.png` 137–331 KB, three `slider1-*.jpg` ~262–304 KB. SVG icon-font sources (`fontawesome-webfont.svg` 442 KB, `themify.svg` 234 KB, `pbmit_gudfin.svg` 160 KB) are legacy icon-font artifacts. **Implication for IMG-01 (Phase 4):** most "imagery" is CSS-background and vendor-owned; the editable surface for IMG-01 is the 12 `<img>` (sizing/proportions/style) plus the inline-style hero/static-box backgrounds in `index.html`. Bulk payload optimization (WebP/AVIF) is **v2 / PERF-01** — out of scope.

### Q3 — Which pages have pricing / FAQ / modal — RESOLVED
[VERIFIED: grep across *.html and js/scripts.js]

- **Pricing / tariffs (CNV-02):** **NONE.** Zero matches for `pricing`, `price-table`, `pbmit-pricing`, `тариф`. No pricing block exists on any of the 11 pages. → CNV-02 in Phase 4 is **net-new**, not "polish existing."
- **FAQ accordion (CMP-05):** **NONE in markup.** Zero matches for `accordion` in any HTML. The theme's accordion handler exists in `js/scripts.js:309` but no page contains `.accordion` markup. → CMP-05 is **feature-absent**; descope or treat as net-new.
- **Modals / Magnific Popup (CMP-06):** Library loaded on all 11 pages (`css/magnific-popup.css`, `js/jquery.magnific-popup.min.js`) and initialized in `js/scripts.js:296-303`, **but gated to triggers `.pbmin-lightbox-video` / `a.pbmit-lightbox` which appear in ZERO markup** (grep = no matches). No lightbox/modal is ever instantiated. → CMP-06 is **feature-absent**; the UI-SPEC already says "Only if Magnific Popup is actually instantiated" — confirmed it is not.

Other component facts for the map: lead `<form class="pfg-form" novalidate>` lives on `contacts.html:256-274` (Name/Phone/biztype select/message/consent checkbox → WhatsApp submit). A Google Maps `<iframe>` is on `contacts.html:288` only.

### Q4 — Fate of chart.js — RESOLVED
[VERIFIED: grep `chart.js`/`chart.min` across *.html = zero matches]

`chart.js` is **not referenced by any of the 11 pages** (no `<script>` includes it). The CLAUDE.md inventory lists it as vendored-but-present in the theme. **Recommendation: keep its removal OUT OF SCOPE** for this milestone — it maps to v2 / PERF-02 (deferred in CONTEXT.md). It contributes zero bytes to the live pages today (not loaded), so it has no perf/CLS impact on the baseline. Document in CONFLICT-CATALOG/IMPL-PLAN as "vendor file, unused, removal deferred to v2."

### Q5 — Real `!important` count in custom.css — RESOLVED
[VERIFIED: grep -c `!important` css/custom.css = **59**]

Exactly **59** — matches the ROADMAP/UI-SPEC `~59` estimate. Use 59 as the CONFLICT-CATALOG baseline and the `!important` budget floor (net-new ≈ 0; each new one must cite the vendor rule it beats).

### Q6 — Audit tooling on Windows no-build — RESOLVED
[VERIFIED: local probes + npm view]

Machine has: Node **v24.11.1**, npm **11.16.0**, npx **11.16.0**, Python **3.14.0** (both `python` and `py`), Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe`. Lighthouse is **not** globally installed (`lighthouse: command not found`) — run via `npx`.

**Practical path for the 11-page baseline (no project build):**
1. Serve: `python -m http.server 8080` from repo root.
2. Perf/CLS/LCP/a11y score: `npx -y lighthouse@13.4.0 http://localhost:8080/<page>.html --output=json --output=html --chrome-flags="--headless=new"` per page, store JSON.
3. WCAG rule violations + DOM-measured visual audit @ 5 viewports: drive the **existing Playwright MCP** (project's established channel) and inject `@axe-core/playwright` for rule checks, or fall back to `npx @axe-core/cli` per URL.
4. All tools are external/ephemeral — nothing is installed into the site, honoring no-build.

PowerShell note (Windows host): run the static server in one shell and audits in another; use `python -m http.server 8080` (not `&`-backgrounding patterns). Chrome flag `--headless=new` is the current headless mode for Chrome.

## Common Pitfalls

### Pitfall 1: Auditing the WhatsApp/form flow as if it could change
**What goes wrong:** Recording "fix form submission" findings.
**Why it happens:** Forms normally have backends; here the form composes a `wa.me` deep link (no backend).
**How to avoid:** visual-only constraint — audit the form's *appearance/states/labels*, never its behavior (VER-04). Behavior is frozen.
**Warning signs:** Any finding that implies changing `initLeadForm` logic.

### Pitfall 2: Counting `!important` in vendor files
**What goes wrong:** Inflated conflict count.
**Why it happens:** Theme CSS has its own `!important`s.
**How to avoid:** The 59 figure is **custom.css only** — the project-owned override budget. Vendor `!important`s are context for the catalog, not part of the project budget.

### Pitfall 3: Treating absent components as present
**What goes wrong:** Writing audit findings for pricing/FAQ/modal that don't exist.
**How to avoid:** Q3 confirms none exist. Record absence; flag CNV-02/CMP-05/CMP-06 as net-new-or-descope for later phases.

### Pitfall 4: Lighthouse against `file://`
**What goes wrong:** Relative paths, `@import` Google Fonts, and the Maps iframe fail or skew metrics under `file://`.
**How to avoid:** Always audit through `http://localhost` (the static server), never by opening the HTML file directly.

### Pitfall 5: Trusting CSS source over rendered DOM
**What goes wrong:** A `custom.css` value looks correct but a vendor media query overrides it at a given viewport.
**How to avoid:** DOM-measured Playwright at each of the 5 viewports (project memory).

## Code Examples

Audit invocation patterns (not site code — this phase writes no site code):

### Per-page Lighthouse baseline
```bash
# Source: https://github.com/GoogleChrome/lighthouse (CLI docs)
python -m http.server 8080   # shell 1, from repo root
npx -y lighthouse@13.4.0 http://localhost:8080/index.html \
  --output=json --output=html \
  --output-path=.planning/phases/01-baseline-audit-ui-design-contract/baseline/index \
  --only-categories=performance,accessibility \
  --chrome-flags="--headless=new"
```

### axe-core via Playwright (a11y rule scan)
```javascript
// Source: https://github.com/dequelabs/axe-core-npm (axe-core/playwright)
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const page = await (await chromium.launch()).newPage();
await page.goto('http://localhost:8080/contacts.html');
const results = await new AxeBuilder({ page }).analyze();
console.log(results.violations); // store per page into AUDIT.md
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Chrome `--headless` | `--headless=new` | Chrome 112+ | Use `--headless=new` for accurate rendering in Lighthouse runs |
| Lighthouse 10/11 | Lighthouse 13.4.0 | 2025–26 | Current metric weightings; pin `@13.4.0` for reproducible floor |

**Deprecated/outdated:** none affecting this phase. The site stack is intentionally frozen.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | npm package ages/download counts for the four audit tools are "high / several years" (not seam-verified, reputation-based) | Package Legitimacy Audit | Low — all are first-party Google/Microsoft/Deque tools, npx-only, nothing installed into repo |
| A2 | `images/` total ≈ 6.9 MB is the full asset weight relevant to IMG-01/PERF-01 | Q2 | Low — IMG-01 is visual-only this milestone; payload is v2 |

**Note:** All six research questions (Q1–Q6) were resolved by reading/grepping the real files — those findings are VERIFIED, not assumed.

## Open Questions

1. **Baseline artifact location vs `.gitignore`**
   - What we know: `.gitignore` excludes Playwright/screenshot audit artifacts at root.
   - What's unclear: Whether the planner wants the Lighthouse JSON/screenshots committed under `.planning/.../baseline/` (likely yes, as the regression floor must persist) or kept local.
   - Recommendation: Store baseline JSON under `.planning/phases/01-*/baseline/` and confirm that path is NOT ignored (it's under `.planning/`, not root) so the floor is committed with the docs.

2. **Known mobile header search target-size flag**
   - What we know: Prior audit (memory `ui-audit-2026-06-23.md`) deliberately left a theme header search target-size flag unfixed.
   - Recommendation: Record it in AUDIT as an accepted documented exception unless this baseline run re-surfaces it as a hard blocker.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | npx Lighthouse/axe/Playwright | ✓ | 24.11.1 | — |
| npm/npx | running audit tools ephemerally | ✓ | 11.16.0 | — |
| Python | local static server | ✓ | 3.14.0 | `npx http-server` |
| Chrome | Lighthouse headless engine | ✓ | installed (path verified) | — |
| Playwright MCP | DOM-measured 5-viewport audit | ✓ (project channel) | 1.61.1 (npm) | `@axe-core/cli` per URL |
| lighthouse | AUD-01 perf/CLS/LCP floor | via npx | 13.4.0 | Chrome DevTools panel (manual, non-reproducible) |
| @axe-core/playwright | AUD-01 a11y rule scan | via npx | 4.12.1 | axe DevTools extension (manual) |

**Missing dependencies with no fallback:** none — every required tool is present or npx-available.
**Missing dependencies with fallback:** Lighthouse not global (use npx); Playwright scripting can fall back to `@axe-core/cli`.

## Security Domain

Not applicable to this phase in the usual sense: it produces documents only, makes no code/auth/data changes, and adds no network-exposed surface. The only outbound calls are the existing Google Fonts `@import` and the Maps `<iframe>` already in the vendored site (unchanged). No secrets are read or written. ASVS categories do not apply to a measurement-and-documentation phase. (Recorded explicitly so the planner does not expect a threat-model section.)

## Sources

### Primary (HIGH confidence)
- Local files: `index.html`, `contacts.html`, `about.html`, `css/base.css`, `css/custom.css`, `css/shortcode.css`, `js/scripts.js` — direct read/grep for Q1–Q5.
- Local probes: `node/npm/npx/python --version`, Chrome path, `images/` listing+sizes — Q2, Q6.
- npm registry (`npm view`): lighthouse 13.4.0, @axe-core/playwright 4.12.1, @axe-core/cli 4.12.1, playwright 1.61.1 — Q6.

### Secondary (MEDIUM confidence)
- GoogleChrome/lighthouse and dequelabs/axe-core-npm CLI/usage patterns (well-known tooling).

### Tertiary (LOW confidence)
- Package age/download estimates in the legitimacy table (reputation-based, not seam-run).

## Metadata

**Confidence breakdown:**
- Resolved questions Q1–Q6: HIGH — every answer verified against real files/probes.
- Audit tooling versions: HIGH — npm view + local probes this session.
- Package legitimacy ages/downloads: LOW — reputation-based; nothing installed into repo so low risk.

**Research date:** 2026-06-26
**Valid until:** 2026-07-26 (stable; site frozen, tool versions may bump — re-pin Lighthouse if reproducibility matters)
