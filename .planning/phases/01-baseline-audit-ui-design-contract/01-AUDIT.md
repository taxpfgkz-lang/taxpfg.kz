# Phase 01 — Baseline Audit & UI Design Contract — AUDIT

**Milestone:** v1.0 — taxpfg.kz Production UI Polish
**Audit date:** 2026-06-26
**Tooling:**
- Lighthouse `13.4.0` (categories: performance, accessibility; Chrome `--headless=new`)
- `@axe-core/playwright` `4.12.1` (axe-core engine `4.12.1`; tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`)
- Served via `python -m http.server 8080` (bound `127.0.0.1`) from the repo root — all audits ran over `http://127.0.0.1:8080/<page>`, never `file://`, so relative `css/js`, `@import` Google Fonts and the Maps iframe resolved and metrics are accurate (RESEARCH Pitfall 4).

**Regression floor statement:** The numbers in the AUD-01 table below are the committed regression floor for **AUD-01**. This is the dependency gate that Phase 5 (A11Y-04, VER-01) is measured against — no later phase may drop a page's accessibility score below the floor recorded here. Raw reports are committed under `baseline/lighthouse/` (11 JSON + 11 HTML) and `baseline/axe/` (11 JSON).

## AUD-01 — Per-page baseline

| Page | A11y score | Perf score | CLS | LCP (ms) | axe violations | axe critical/serious IDs |
|------|-----------:|-----------:|----:|---------:|---------------:|--------------------------|
| index.html               | 96 | 55 | 0.077 | 15392 | 0 | none |
| about.html               | 95 | 57 | 0.000 |  9158 | 0 | none |
| services.html            | 96 | 56 | 0.000 | 10070 | 0 | none |
| accounting.html          | 95 | 56 | 0.000 |  9924 | 0 | none |
| accounting-recovery.html | 95 | 56 | 0.000 |  9768 | 0 | none |
| taxes.html               | 95 | 56 | 0.000 |  9920 | 0 | none |
| consulting.html          | 95 | 56 | 0.000 |  9928 | 0 | none |
| registration.html        | 95 | 56 | 0.000 |  9761 | 0 | none |
| contacts.html            | 96 | 56 | 0.000 |  9996 | 0 | none |
| privacy.html             | 95 | 56 | 0.000 |  9760 | 0 | none |
| 404.html                 | 95 | 56 | 0.000 |  9779 | 0 | none |

**Floor note:**
- **Minimum accessibility score across the 11 pages = 95** (all content pages except `index.html`, `services.html`, `contacts.html` which score 96). No later phase may drop any page below its row value here; the hard a11y floor is **95**.
- **axe-core (WCAG 2.0/2.1 A + AA): zero violations on all 11 pages.** This is a clean WCAG floor — Phase 5 must keep it at zero for the scanned tag set.
- **Performance** sits at 55–57 across the board. This is *not* a regression gate for this milestone (the milestone is UI polish, not perf), but it is recorded for reference. `index.html` LCP (~15.4 s) is the outlier (hero slider); all inner pages cluster ~9–10 s. CLS is effectively 0 everywhere except `index.html` (0.077, still within Lighthouse "good" < 0.1).

### Known accepted exception (not a new violation)

The previously documented **mobile header search target-size** flag (theme-owned, accepted exception per RESEARCH Open Question 2 and MEMORY `ui-audit-2026-06-23`) did **not** surface in this axe run because it maps to **WCAG 2.2 SC 2.5.8 (Target Size, Minimum)**, which is outside the `wcag2a/2aa/21a/21aa` tag set scanned here. It is therefore not counted in the 0-violation floor above. Plan 01-03 should log it as a standing exception rather than new work, unless it surfaces as a hard blocker.

### Reproduce

```bash
# from repo root
python -m http.server 8080 --bind 127.0.0.1   # one shell

# Lighthouse (per page; <slug> = filename without .html, 404 for 404.html)
npx -y lighthouse@13.4.0 http://127.0.0.1:8080/<slug>.html \
  --output=json --output=html \
  --output-path=.planning/phases/01-baseline-audit-ui-design-contract/baseline/lighthouse/<slug> \
  --only-categories=performance,accessibility --chrome-flags="--headless=new"

# axe-core via @axe-core/playwright 4.12.1 (ephemeral runner; tags wcag2a/2aa/21a/21aa)
```

> Windows/Cyrillic-path note: Lighthouse prints a non-fatal `EPERM ... rmSync` at temp **cleanup** (`chrome-launcher destroyTmp`) *after* the report is already saved. The JSON/HTML reports are complete and valid; the error is cosmetic temp-dir teardown only.

## AUD-02 — Visual problems by block-type

Filled by plan 01-03
