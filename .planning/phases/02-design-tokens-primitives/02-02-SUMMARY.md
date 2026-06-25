---
phase: 02-design-tokens-primitives
plan: 02
subsystem: ui
tags: [css, design-tokens, spacing-snap, fluid-typography, line-height-policy, text-wrap, a11y, ios-zoom]

# Dependency graph
requires:
  - phase: 02-design-tokens-primitives
    provides: "02-01 token sheet (--pfg-space-*, --pfg-fs-*, --pfg-lh-*) declared additively"
  - phase: 01-baseline-audit-ui-design-contract
    provides: "AUD-01 a11y floor (min 95, axe color-contrast 0), AUD-02 findings (C1/F1/HE1/T2/G2/P2), !important budget floor 59"
provides:
  - "Card padding snapped 28→24px via var(--pfg-space-6) at both .pfg-card and .pbmit-box-content-wrap"
  - "Mobile .form-control font-size 16px (iOS<16 focus-zoom suppressed) via .pfg-form hook, no !important"
  - "Heading line-height policy: no clamped/vendor heading renders lh<fs (hero, title-bar, tween headline)"
  - "Fluid body type wired to var(--pfg-fs-body)/var(--pfg-lh-body) on .pfg-lead/.pfg-prose"
  - "text-wrap: balance (headings) + pretty (body) orphan/widow guard"
affects: [03-components, 04-conversion-blocks]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Vendor line-height override wins by SOURCE-ORDER at equal/greater specificity (custom.css loads last), never by net-new !important"
    - "Unitless --pfg-lh-display (1.15) scales with every responsive font-size tier so lh>=fs holds at 1440/1024/768/390/360"
    - ".pfg-* rules that already own size consume var() tokens directly (declaration→application link)"

key-files:
  created:
    - .planning/phases/02-design-tokens-primitives/02-02-SUMMARY.md
  modified:
    - css/custom.css

key-decisions:
  - "Card padding snapped to --pfg-space-6 (24px) in both documented C1 locations; no other padding touched (02-RESEARCH Pitfall 2)"
  - "F1 input font-size:16px placed on existing .pfg-form .form-control hook — wins by specificity 0,2,0 > vendor 0,1,0 + source-order, no !important"
  - "Line-height policy applied at vendor selector specificity for hero (0,2,0), title-bar (0,1,0), and tween headline (0,3,0); all source-order wins, budget stayed 59"
  - ".pbmit-tween-effect-style-1 headline (170/142, lh<fs) was an undocumented offender the plan's action step omitted (named only hero) — fixed under deviation Rule 1 (checker requires lh>=fs on every visible heading)"
  - "Russian preposition per-word non-breaking DEFERRED (needs &nbsp; in read-only markup or JS) — only text-wrap balance/pretty delivered, as the plan locked"
  - "VIS-02 title-bar T1 (fixed 550px min-height) recorded out-of-scope: it is a height-tier change, not a spacing-token snap; locked out of this phase"

patterns-established:
  - "Pattern: heading line-height floor via unitless token at vendor specificity + source-order (no !important growth)"
  - "Pattern: durable Playwright DOM-measured + axe + Lighthouse + JS-smoke verification channel re-used from AUD-01"

requirements-completed: [TOK-02, TOK-03, VIS-02, VIS-03]

coverage:
  - id: A1
    description: "Card padding snapped 28→24px (var(--pfg-space-6)) at .pfg-card and .pbmit-box-content-wrap; DOM paddingTop==24 at all 5 widths"
    requirement: "TOK-02"
    verification:
      - kind: dom-measure
        ref: "Playwright getComputedStyle paddingTop == 24px at 1440/1024/768/390/360 on index/contacts/services"
        status: pass
    human_judgment: false
  - id: A2
    description: "Mobile .form-control font-size >=16px on contacts.html (iOS focus-zoom suppressed), no new !important"
    requirement: "TOK-03"
    verification:
      - kind: dom-measure
        ref: "Playwright fontSize == 16 @390/360 on contacts.html; grep -c '!important' == 59"
        status: pass
    human_judgment: false
  - id: A3
    description: "No heading renders lh<fs at desktop worst-case (1440) or mobile (390): hero, title-bar, tween headline all lh>=fs"
    requirement: "TOK-03"
    verification:
      - kind: dom-measure
        ref: "Playwright worst-heading ratio >= 1.0 at all 5 widths after tween fix (was 0.835)"
        status: pass
    human_judgment: false
  - id: A4
    description: "Fluid body type applied: .pfg-lead fontSize scales 18px(1440)→16.2px(390) within clamp; text-wrap balance/pretty present"
    requirement: "TOK-03"
    verification:
      - kind: dom-measure
        ref: "Playwright leadFontSize 18 @1440 vs 16.175 @390 (scales:true); grep text-wrap balance+pretty"
        status: pass
    human_judgment: false
  - id: A5
    description: "Contrast no-regression: axe color-contrast == 0 on all 11 pages; no gold #ecab23 as body text"
    requirement: "VIS-03"
    verification:
      - kind: other
        ref: "axe-core wcag2a/2aa/21a/21aa: 0 color-contrast, 0 total on 11 pages; grep no color:#ecab23"
        status: pass
    human_judgment: false
  - id: A6
    description: "No new horizontal scroll; a11y >= AUD-01 floor; JS behaviors identical (VER-04)"
    verification:
      - kind: dom-measure
        ref: "scrollWidth<=clientWidth all 5 widths; Lighthouse a11y matches AUD-01 row per page (min 95); VER-04 menu/float/form-wa-link/swiper/reduced-motion all pass"
        status: pass
    human_judgment: false

# Metrics
duration: 20min
completed: 2026-06-25
status: complete
---

# Phase 2 Plan 02: Apply Tokens to AUD-02 Findings Summary

**Applied the 02-01 tokens to the four AUD-02 findings — card padding snap (28→24px), 16px mobile input (iOS zoom kill), heading line-height policy (no lh<fs anywhere), and fluid body type + text-wrap — then proved zero regression against the Phase-1 floor via DOM-measured Playwright, axe (11 pages), Lighthouse, and a VER-04 JS smoke, all without growing the !important budget past 59.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-06-25T21:56:06Z
- **Completed:** 2026-06-25T22:16:26Z
- **Tasks:** 3
- **Files modified:** 1 (css/custom.css)

## Accomplishments
- **C1 / TOK-02:** `.pfg-card` (custom.css:67) and `.pbmit-element-service-style-2 .pbmit-box-content-wrap` (custom.css:~893) padding swapped from literal `28px` to `var(--pfg-space-6)` (24px). DOM-measured `paddingTop == 24` at all 5 widths.
- **F1 / TOK-03:** `.pfg-form .form-control/.form-select/textarea` now declares `font-size:16px` — wins by specificity 0,2,0 over vendor `.form-control` 0,1,0 (style.css:2641) + source-order, **no `!important`**. DOM-measured `16px` at 390/360 on contacts.html.
- **HE1/T2/G2 / TOK-03:** Heading line-height policy via unitless `--pfg-lh-display` (1.15) on three vendor selectors: hero `.pbmit-slider-one .pbmit-slider-title` (was 170/150), title-bar `.pbmit-tbar-title` (was 70/70), and the tween headline `.pbmit-tween-effect-style-1 .pbmit-element-title` (was 170/142). After the fix, the worst heading ratio at every width is >= 1.0 (no lh<fs).
- **TOK-03 fluid type:** `.pfg-lead` / `.pfg-prose p` wired to `var(--pfg-fs-body)` / `var(--pfg-lh-body)`. DOM-measured `.pfg-lead` scales 18px @1440 → 16.2px @390 (fluid, within clamp).
- **TOK-03 wrapping:** `text-wrap: balance` on `.pfg-card h3`, `text-wrap: pretty` on `.pfg-lead` / `.pfg-prose p`.
- **VIS-03:** No rule introduces gold `#ecab23` as body text; axe color-contrast = 0 on all 11 pages (== AUD-01 floor).
- **VER-04:** Menu open/close, WhatsApp float link, lead-form → WhatsApp deep link (same number `77072370050` + full message), 3/3 Swipers init, reduced-motion preserves all 3 brand Swipers — all behavior-identical (js/custom.js untouched, git-confirmed).

## Verification Record (real measured numbers)

### DOM measurements (Playwright, rendered box) — index.html / contacts.html / services.html @ 1440/1024/768/390/360
| Assertion | Result |
|-----------|--------|
| `.pfg-card` / `.pbmit-box-content-wrap` paddingTop | **24px** at all 5 widths, all 3 pages |
| `.form-control` fontSize @390/360 (contacts.html) | **16px** |
| Worst heading lineHeight/fontSize ratio (all widths) | **>= 1.0** (was 0.835 before tween fix) — hero, title-bar, tween headline all lh>=fs |
| Hero `.pbmit-slider-title` fontSize @1440 | **170px** (unchanged — Phase 2 = lh policy only, hero height = Phase 4) |
| `.pfg-lead` fontSize 1440 → 390 | **18 → 16.175px** (fluid, scales:true) |
| `documentElement.scrollWidth <= clientWidth` | **true** at all 5 widths (no horizontal overflow) |
| WhatsApp float tap target | **56×56px** (>= 44, unchanged) |

### axe-core (wcag2a/2aa/21a/21aa) — 11 pages @ 1440
- **color-contrast violations: 0** on every page (index, about, services, accounting, accounting-recovery, taxes, consulting, registration, contacts, privacy, 404)
- **total violations: 0** — exactly matches the AUD-01 clean floor

### Lighthouse accessibility — 11 pages (matches AUD-01 row exactly, zero regression)
| Page | a11y | AUD-01 floor |
|------|------|--------------|
| index.html | 96 | 96 |
| about.html | 95 | 95 |
| services.html | 96 | 96 |
| accounting.html | 95 | 95 |
| accounting-recovery.html | 95 | 95 |
| taxes.html | 95 | 95 |
| consulting.html | 95 | 95 |
| registration.html | 95 | 95 |
| contacts.html | 96 | 96 |
| privacy.html | 95 | 95 |
| 404.html | 95 | 95 |

### VER-04 JS smoke (js/custom.js byte-identical — git-confirmed untouched)
| Behavior | Result |
|----------|--------|
| WhatsApp float renders + links | `https://wa.me/77072370050` ✓ |
| Mobile menu toggle (#menu-toggle) | opens on click, closes on Esc ✓ |
| Lead form → WhatsApp deep link | same number `77072370050`, message `Здравствуйте! Заявка с сайта taxpfg.kz.\nИмя: …\nТелефон: …` ✓ |
| Swiper sliders initialized | 3/3 ✓ |
| Reduced-motion (prefers-reduced-motion: reduce) | all 3 brand Swipers still init ✓ |

### Budget gate
- `grep -c '!important' css/custom.css` = **59** (no net-new; AUD-03 floor held)

## Task Commits

1. **Task 1: Snap card padding to token + input font-size 16px (TOK-02/F1)** - `49ec60e` (feat)
2. **Task 2: Heading line-height policy + fluid body type + text-wrap (TOK-03/VIS-03)** - `4ee9343` (feat)
3. **Task 3 fix: Extend line-height policy to tween headline (HE1/G2)** - `d1dee66` (fix)

**Plan metadata:** committed separately with SUMMARY/STATE/ROADMAP.

## Files Created/Modified
- `css/custom.css` - card padding token (×2), input font-size, hero/title-bar/tween line-height policy, fluid body type, text-wrap balance/pretty (37 insertions, 5 deletions across 3 commits)

## Decisions Made
- Line-height policy enforced strictly by source-order at vendor specificity — the desktop hero/title-bar/tween overrides win without a new `!important` (02-RESEARCH Pitfall 3 honored). Budget verified at 59 after each task.
- Fluid `.pfg-lead` desktop max (18px clamp) equals the prior fixed 18px, so desktop is non-regressive while mobile gains fluidity.
- The pre-existing `@max-575` hero `!important` overrides (custom.css:182-183) were left untouched; the unitless line-height on the base selector composes correctly with them at mobile.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Missing coverage] Tween headline line-height not in plan's action step**
- **Found during:** Task 3 DOM verification
- **Issue:** The plan's Task 2 action named only the hero `.pbmit-slider-title` for the line-height policy, but DOM measurement found `.pbmit-tween-effect-style-1.pbmit-tween-text .pbmit-element-title` rendering 170px/142px (ratio 0.835, lh<fs) at every width. The Task 3 checker requires `lineHeight >= fontSize` on **every** visible heading, so this was an in-scope correctness gap, not new scope.
- **Fix:** Added `line-height: var(--pfg-lh-display)` on the tween selector at its native 0,3,0 specificity. Source-order win over responsive.css tiers (135/111, 100/80, 70/58), unitless value scales with each tier. No `!important`.
- **Files modified:** css/custom.css
- **Commit:** d1dee66

### Recorded out-of-scope (not fixed, by lock)

**VIS-02 title-bar T1 (fixed 550px min-height tier).** AUD-02 T1 flags the 550px title-bar band as disproportionate at 768px. This is a height-tier change, not a pure spacing-token snap, and the phase is locked to spacing-token application + line-height policy only (no vendor-grid/height restructuring). Recorded for a later VIS/hero-polish phase. The title-bar's documented spacing override (custom.css:957-972, mobile) was left as-is.

## Known Stubs / Deferred

**Russian preposition per-word non-breaking — DEFERRED (out of scope, markup/JS).** CSS alone cannot force a short preposition/conjunction (в, и, с, к, на, по, от) off a line-end. This requires `&nbsp;` in the read-only markup or a JS text pass — neither is in scope this phase (markup read-only, js/custom.js not edited). Delivered instead: `text-wrap: balance` (headings) + `text-wrap: pretty` (body) as the CSS-only orphan/widow guard (~88% browser support, graceful degrade). 02-RESEARCH Open Question 1 / Pitfall 4.

## Issues Encountered
- Initial VER-04 smoke failures were test-harness selector/timing assumptions (wrong toggle id, `.swiper` vs `.swiper-slider`, click-vs-dispatch), not site regressions — corrected the test to match actual markup; all behaviors then verified identical. Temp verification scripts were removed after the run.

## User Setup Required
None — no external service configuration. Verification used a local `python -m http.server 8080` and Playwright/axe/Lighthouse run ephemerally (installed with `--no-save`, no project manifest change since the site has no package.json).

## Next Phase Readiness
- Tokens are now applied to the AUD-02 findings with the Phase-1 a11y/contrast/overflow floor intact. Phase 3 (components) and Phase 4 (conversion blocks + hero height/LCP) can build on the spacing scale and line-height policy.
- No blockers. Deferred items: preposition non-breaking (markup/JS), title-bar 550px height tier (VIS/hero phase).

---
*Phase: 02-design-tokens-primitives*
*Completed: 2026-06-25*

## Self-Check: PASSED
- 02-02-SUMMARY.md present
- Commits 49ec60e, 4ee9343, d1dee66 all exist in git
- css/custom.css carries applied tokens: `padding:var(--pfg-space-6)`, `var(--pfg-fs-body)`, `text-wrap` balance/pretty, line-height policy on hero/title-bar/tween
- `grep -c '!important'` = 59 (budget held)
