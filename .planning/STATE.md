---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
last_updated: "2026-06-27T00:31:58.961Z"
last_activity: 2026-06-27
progress:
  total_phases: 5
  completed_phases: 3
  total_plans: 13
  completed_plans: 11
  percent: 60
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-25)

**Core value:** Сайт выглядит дорого, единообразно и убедительно на desktop/tablet/mobile, а conversion-блоки чисто конвертируют посетителя в лид — без изменения бизнес-логики.
**Current focus:** Phase 4 — Conversion Blocks + Imagery

## Current Position

Phase: 4 (Conversion Blocks + Imagery) — EXECUTING
Plan: 3 of 4
Status: Ready to execute
Last activity: 2026-06-28 — Quick task 260628-h3e (Волна 1 конверсии: мобильный контакт + sticky CTA)

Progress: [█████████░] 85%

## Performance Metrics

**Velocity:**

- Total plans completed: 9
- Average duration: — min
- Total execution time: 0.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 | 4 | - | - |
| 2 | 2 | - | - |
| 3 | 3 | - | - |

**Recent Trend:**

- Last 5 plans: —
- Trend: —

*Updated after each plan completion*
| Phase 01 P01 | 8min | 3 tasks | 23 files |
| Phase 01 P02 | 8min | 2 tasks | 1 files |
| Phase 01 P03 | 25min | 2 tasks | 38 files |
| Phase 01 P04 | 14m | 2 tasks | 2 files |
| Phase 02 P01 | 6min | 1 tasks | 1 files |
| Phase 02 P02 | 20min | 3 tasks | 1 files |
| Phase 03 P01 | 18min | 3 tasks | 1 files |
| Phase 03 P02 | 18min | 3 tasks | 3 files |
| Phase 03 P03 | 32min | 3 tasks | 0 files |
| Phase 04 P01 | 20min | 2 tasks | 2 files |
| Phase 04 P02 | 2min | 2 tasks | 1 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Audit-first — Phase 1 produces documents only; no code edits until plan + UI design contract are approved.
- [Roadmap]: Strict bottom-up build order — tokens (P2) are the root dependency; components (P3), then conversion blocks (P4), then a11y/verification (P5).
- [Roadmap]: `@layer` is FORBIDDEN for theme overrides (unlayered vendor always wins) — overrides win by source-order + targeted specificity only.
- [Roadmap]: AUD-01 baseline is the dependency gate for all verification (A11Y-04, VER-01); capture before any edit.
- [Phase ?]: AUD-01 baseline floor captured: min a11y=95, axe WCAG 2.0/2.1 A+AA=0 violations across 11 pages (lighthouse@13.4.0, axe-core 4.12.1)
- [Phase ?]: WCAG 2.2 target-size flag (SC 2.5.8) recorded as accepted exception, outside scanned axe tags
- [Phase ?]: AUD-03: !important budget floor = 57 функциональных деклараций (grep-c=59 сверен); chart.js удаление → v2/PERF-02
- [Phase ?]: AUD-02 visual problems enumerated by block-type from DOM measurement (103 boxes, 5 viewports), not CSS source text
- [Phase ?]: Baseline screenshots force-committed under baseline/screenshots/ as required audit evidence (T-01-03); generic screenshots/ ignore left intact for ad-hoc shots
- [Phase ?]: 01-UI-SPEC.md verified complete against AUD-04 and signed off (Approval approved); AUD-01 had 0 axe contrast violations so no contrast gap to close
- [Phase ?]: Pricing/FAQ/modal marked NET-NEW for Phases 3-4 (CMP-06 conditioned on Magnific Popup instantiation); target-size accepted exception; chart.js out-of-scope v2/PERF-02
- [Phase ?]: [Phase 2 P01]: Токены объявлены аддитивно в :root (custom.css); существующие --pfg-* байт-идентичны; clamp() maxes зеркалят vendor desktop-px (h1 58..h6 22) — desktop без регрессии; z-index:9999 -> --pfg-z-float (единственный consumer); !important остаётся 59
- [Phase ?]: 02-02: line-height policy via unitless --pfg-lh-display at vendor specificity + source-order, no net-new !important (budget 59)
- [Phase ?]: 02-02: Russian preposition non-breaking DEFERRED (markup/JS); delivered text-wrap balance/pretty
- [Phase ?]: Ghost-tier (.pbmit-btn.pfg-ghost): hover = золотая подложка rgba(.12), не заливка — заливка зарезервирована за primary
- [Phase ?]: C2 height-jitter — не min-height-баг: same-row spread=0px на всех ширинах (DOM-замер), min-height не добавлен, только align-items:stretch
- [Phase ?]: Бюджет !important — литеральный grep: в комментариях избегать токена !important, формулировать «без форсирования каскада»
- [Phase ?]: [Phase 3 P03]: Phase-gate доказан DOM-измерением — 55 комбинаций без h-скролла, axe=0+color-contrast=0 на 11, Lighthouse a11y=floor (min 95), FT1/F2>=44px, FAQ клик+клавиатура+focus-ring, VER-04 behavior-identical, !important=59 — floor для Phase 5
- [Phase ?]: [Phase 4 P01]: CNV-02 pricing — 3 тарифа на services.html, ровно один золотой highlight (ТОО на общем режиме); цены индикативные (от …₸/по запросу), точные → v2; per-tier CTA wa.me direct-link (target=_blank rel=noopener), без JS; !important=59 (no net-new); только services.html+custom.css, js байт-идентичен; Playwright PASS на 5vp
- [Phase ?]: CNV-01 подтверждён без правок: Phase-2 политика --pfg-lh-display уже даёт lh>=fs в hero (DOM-замер Playwright 1440:170/195.5, 1024:120/138)
- [Phase ?]: CNV-03 закрыт по отсутствию: sticky мобильной CTA нет, .pfg-whatsapp-float — единственный float, коллизия невозможна; комментарий в custom.css, js байт-идентичен
- [Quick 260628-h3e]: CNV-03 SUPERSEDED — введена мобильная sticky CTA-полоса (≤576px, всегда видима) + контакт tel/WhatsApp в шапке (577–1200px); инжект из общего custom.js (0 правок в 11 HTML), float скрыт ≤1200. Ради конверсии под рекламный трафик (docs/REDESIGN-BRIEF.md, Волна 1). D7 (обрезка заголовков услуг) — DOM-замером подтверждено отсутствие (flow-root), кода нет.

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

- ✓ RESOLVED in Phase 1: font-loading config (@import base.css:16-19), img inventory (12 <img>, CSS-bg dominant), pricing/FAQ/modal (all absent → net-new), chart.js (unused → out-of-scope v2).
- **SCOPE CHANGE 2026-06-26 (Phase 3):** markup-read-only LIFTED by Юрий — HTML edits allowed broadly (unblocks FAQ/pricing net-new). Vendor read-only (swiper-*/data-aos*/pbmit-*, vendor files) STILL holds; VER-04 behavior-identity (form→WhatsApp/analytics/routing/JSON-LD) STILL hard; shared chrome = change-all-11 atomic.
- No automated tests exist — Playwright DOM-measured checks + axe/Lighthouse are the only QA. Workflow API proxy may fail (memory note); duplicate critical checks manually.
- Known accepted exception: mobile header search target-size flag (theme off-canvas layout) — not a new violation.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260628-h3e | Волна 1 конверсии — мобильный контакт в шапке + sticky CTA + D7 verify | 2026-06-28 | c0a8bc7 | [260628-h3e-1-sticky-cta](./quick/260628-h3e-1-sticky-cta/) |

## Deferred Items

Items acknowledged and carried forward from previous milestone close:

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| Performance | Image optimization (WebP/AVIF, srcset) — PERF-01 | Deferred to v2 | 2026-06-25 |
| Performance | Remove unused vendor libs (chart.js 208KB) — PERF-02 | Deferred to v2 | 2026-06-25 |
| Performance | Font-loading optimization (font-display/preload) — PERF-03 | Deferred to v2 | 2026-06-25 |
| Maintainability | Header/footer templating to kill ×11 duplication — MNT-01 | Deferred to v2 | 2026-06-25 |

## Session Continuity

Last session: 2026-06-27T00:31:40.993Z
Stopped at: Completed 04-01-PLAN.md
Resume file: None
