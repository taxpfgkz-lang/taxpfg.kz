---
phase: 04-conversion-blocks-imagery
plan: 02
subsystem: ui
tags: [hero, swiper, line-height, cta, whatsapp-float, conversion]

# Dependency graph
requires:
  - phase: 02-typography-rhythm
    provides: "--pfg-lh-display (1.15) line-height policy applied to hero slider-title and tween title"
  - phase: 03-buttons-hierarchy
    provides: "button hierarchy (one prominent primary per screen)"
  - phase: 04-01
    provides: "pricing block delivering site-wide CTA hierarchy"
provides:
  - "CNV-01 confirmed: hero heading lh >= fs at 1440/1024, exactly one CTA per slide, no horizontal overflow — by Playwright DOM measurement, no code change needed"
  - "CNV-03 closed by documented absence: no sticky mobile CTA exists; .pfg-whatsapp-float is the only floating element and collides with nothing"
affects: [04-04, verification]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Resolution-by-absence: a non-existent risk (sticky-CTA collision) closed by a documented code comment + verified grep, not by adding code"

key-files:
  created: []
  modified:
    - css/custom.css

key-decisions:
  - "Task 1 added NO new CSS rule — the Phase-2 --pfg-lh-display policy already yields lh>=fs (1440: 170/195.5; 1024: 120/138). Adding a redundant rule would violate the plan's 'only if a rendered defect is found' gate."
  - "CNV-03 documented as a code comment beside .pfg-whatsapp-float (comment only, no rule, no !important, no render impact); js/custom.js left byte-identical."

patterns-established:
  - "Confirm-before-edit: DOM-measure the existing render first; if the invariant already holds, record 'confirmed, no change' rather than re-asserting it in CSS."

requirements-completed: [CNV-01, CNV-03]

coverage:
  - id: D1
    description: "Hero heading line-height >= font-size at 1440 and 1024 (2-line Cyrillic title never clips)"
    requirement: "CNV-01"
    verification:
      - kind: automated_ui
        ref: "playwright DOM: .pbmit-slider-one .pbmit-slider-title computed lh>=fs — 1440: fs170/lh195.5; 1024: fs120/lh138 (all lhGteFs=true)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Each hero slide shows exactly one CTA (no competing primary)"
    requirement: "CNV-01"
    verification:
      - kind: automated_ui
        ref: "playwright DOM: .pbmit-slider-one .swiper-slide .pbmit-btn count = [1,1,1,1,1] at 1440 and 1024 (5 = 3 slides + 2 Swiper loop-clones)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Hero reads above the fold with no horizontal overflow"
    requirement: "CNV-01"
    verification:
      - kind: automated_ui
        ref: "playwright DOM: documentElement.scrollWidth == clientWidth at 1440 and 1024 (hasHScroll=false)"
        status: pass
    human_judgment: false
  - id: D4
    description: "CNV-03 closed by documented absence — no sticky mobile CTA exists; .pfg-whatsapp-float is the sole floating element; no collision possible; js byte-identical"
    requirement: "CNV-03"
    verification:
      - kind: automated_ui
        ref: "grep: only project position:fixed is .pfg-whatsapp-float (custom.css:25; lines 429/1175 are vendor off-canvas comments); no sticky-cta/cta-bar/mobile-cta markup in any *.html; no position:sticky in custom.css; git diff HEAD js/custom.js empty"
        status: pass
    human_judgment: false

# Metrics
duration: 2min
completed: 2026-06-27
status: complete
---

# Phase 4 Plan 2: Hero Polish (CNV-01) + CNV-03 Resolution-by-Absence Summary

**Hero confirmed production-clean via Playwright DOM (lh>=fs, one CTA/slide, no overflow) requiring zero new CSS; CNV-03 closed by a documented-absence comment proving no sticky-CTA collision can exist.**

## Performance

- **Duration:** 2 min
- **Started:** 2026-06-27T00:28:30Z
- **Completed:** 2026-06-27T00:30:22Z
- **Tasks:** 2
- **Files modified:** 1 (css/custom.css — comment only)

## Accomplishments
- **CNV-01 confirmed without a code change.** Playwright DOM measurement shows the Phase-2 `--pfg-lh-display` (1.15) policy already keeps the 2-line Cyrillic hero title from clipping: at 1440 `font-size:170 / line-height:195.5`, at 1024 `120 / 138` — `lh >= fs` on every measured title. Per the plan's explicit gate ("add NO new rule" if lh>=fs already holds), no rule was added.
- **One CTA per slide confirmed.** `.pbmit-btn` count per `.swiper-slide` = `[1,1,1,1,1]` at both viewports (5 = 3 authored slides + 2 Swiper loop-clones). No competing primary CTA introduced; hero copy untouched (VER-04).
- **No horizontal overflow** at 1440 or 1024 (`scrollWidth == clientWidth`).
- **CNV-03 closed by documented absence.** A banner comment was added beside `.pfg-whatsapp-float` recording that no sticky mobile CTA exists, so the anticipated sticky-CTA ↔ float collision physically cannot occur. Verified by grep: the only project-authored `position:fixed` is `.pfg-whatsapp-float`; no `sticky-cta`/`cta-bar`/`mobile-cta` markup in any HTML; no `position:sticky` in custom.css. `js/custom.js` is byte-identical.

## Task Commits

1. **Task 1: Confirm/extend hero visual polish (CNV-01)** — no commit (confirmed by DOM measurement; the Phase-2 lh policy already satisfies lh>=fs, so per plan no CSS rule was added and nothing was committed for this task).
2. **Task 2: Resolve CNV-03 by documented absence** — `fb90d74` (docs)

_No Task 1 commit is correct, not an omission: the plan instructs adding a rule "only if a genuine rendered defect is found." None was found._

## Files Created/Modified
- `css/custom.css` — added a 10-line Russian comment beside `.pfg-whatsapp-float` documenting the CNV-03 resolution-by-absence. No selector/rule/`!important` added; zero render impact.

## CNV-03 Resolution-by-Absence (explicit record)

Per the plan's five required points:
1. **No sticky mobile CTA exists on the site.** Grep across all 11 HTML files finds no `sticky-cta`, `cta-bar`, `mobile-cta`, or `pfg-sticky` markup; custom.css has no `position:sticky`.
2. **The anticipated sticky-CTA ↔ `.pfg-whatsapp-float` collision physically cannot occur** — there is no second fixed/sticky element to overlap with.
3. **`.pfg-whatsapp-float` is the sole project-authored floating element** (`position:fixed`, bottom-right, `custom.css:25`) and overlaps nothing at 390/360. (custom.css lines 429/1175 referencing `position:fixed` are comments describing the *vendor* off-canvas menu, not project floats.)
4. **Site-wide CTA hierarchy** (one prominent primary per screen) is already delivered through Phase-2 tokens + Phase-3 button hierarchy + the Plan 04-01 pricing block — no additional sticky CTA is introduced, by design.
5. **`js/custom.js` is byte-identical** (`git diff HEAD -- js/custom.js` empty) — VER-04 satisfied.

## Decisions Made
- Did not add a redundant hero line-height rule. The existing Phase-2 policy is sufficient (DOM-verified), and the plan forbids adding a rule absent a real rendered defect.
- Recorded CNV-03 as a code comment (durable, in-context for future readers) rather than leaving the absence implicit only in the SUMMARY.

## Deviations from Plan

None - plan executed exactly as written.

## Pre-existing Notes (flagged, not changed)
- **Hero markup typo (index.html:169-171):** Slide 1 opens `<h2 class="pbmit-slider-title">` and closes `</h1>`. This is pre-existing vendor/authored markup and was NOT touched (VER-04 + 04-RESEARCH Pitfall 2). Flagged here for visibility; browsers auto-correct the mismatched tag and it does not affect the hero render or the CTA/lh measurements above. Any fix belongs to a deliberate, separately-scoped markup task.
- **Uncommitted index.html working-tree changes** exist from prior work (nav label, sr-only H1 text, about-section headings, footer widget `active` class). None are in the hero block (160-258) and none were made by this plan. The hero markup is verified untouched.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Hero (top conversion surface) verified production-clean; CNV-01 and CNV-03 closed.
- Wave-4 verification plan can re-confirm hero lh/CTA invariants against the same DOM checks recorded here.

## Self-Check: PASSED
- css/custom.css comment present; commit fb90d74 exists; SUMMARY on disk.
- !important = 59 (unchanged); js/custom.js byte-identical; hero markup untouched.

---
*Phase: 04-conversion-blocks-imagery*
*Completed: 2026-06-27*
