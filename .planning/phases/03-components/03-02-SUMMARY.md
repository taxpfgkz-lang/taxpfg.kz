---
phase: 03-components
plan: 02
subsystem: ui
tags: [faq, details-summary, a11y, tap-target, wcag-2.5.5, css-cascade, no-build, static-site]

# Dependency graph
requires:
  - phase: 02-tokens
    provides: "--pfg-* токены (space/fs/lh/gold/hairline/shadow/ease) — питают FAQ-стили и тап-зоны"
  - phase: 03-01
    provides: "Этап 14 секция custom.css (CMP-01..04 + C2), куда дописаны 14.7-14.10"
provides:
  - "FAQ-аккордеон (CMP-05) на services.html и contacts.html — native <details>/.pfg-faq, клавиатура+ARIA из коробки"
  - "FT1 устранён: тап-зона футер-ссылок ОБЕИХ колонок (Разделы+Услуги) >=44px @390/360"
  - "F2 устранён: хит-зона лейбла .pfg-consent >=44px"
  - "CMP-06 модалки честно descoped (Magnific не инстанцирован, 0 триггеров)"
affects: [03-03, phase-04-conversion, phase-05-final-a11y]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Native <details>/<summary> для аккордеона — нулевая связь с theme-handler (класс .pfg-faq, НЕ .accordion)"
    - "Root-cause тап-таргет фикс через общий предок селектора, DOM-измерение ОБЕИХ групп перед финализацией"
    - "Descope через документацию-маркер в CSS (удовлетворение через отсутствие)"

key-files:
  created: []
  modified:
    - "services.html — net-new FAQ <section> .pfg-faq перед </main>"
    - "contacts.html — net-new FAQ <section> .pfg-faq перед формой"
    - "css/custom.css — 14.7 FAQ-стили, 14.8 FT1, 14.9 F2, 14.10 CMP-06 descope; summary в focus-visible группе; chevron в reduced-motion"

key-decisions:
  - "Native <details>/<summary> вместо button+region — клавиатура/[open]/AT-семантика бесплатно, ноль связи с theme-handler scripts.js:309"
  - "initFaqA11y НЕ добавлен — native <details> самодостаточен; js/custom.js байт-идентичен (VER-04 сохранён)"
  - "FT1 фикс на общий предок .site-footer .widget ul.menu li a — DOM подтвердил, что 26px читает только колонка Разделы (Услуги уже 46.5px)"

patterns-established:
  - "FAQ: <details class='pfg-faq-item'> > summary + div.pfg-faq-panel; chevron через ::after, поворот на [open]"
  - "Тап-таргет фикс: измерить getBoundingClientRect ДО фикса, целиться в общий предок, перепроверить @390/360"

requirements-completed: [CMP-05, CMP-06]

coverage:
  - id: D1
    description: "FAQ-аккордеон (CMP-05): native <details>/.pfg-faq на services.html и contacts.html, 5 Q&A каждая, не .accordion"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: services.html FAQ — click toggle open=true→false, Enter toggle, Space toggle, panel visible"
        status: pass
      - kind: other
        ref: "grep: pfg-faq на 2 страницах, 0 на остальных 9; class=accordion = 0"
        status: pass
    human_judgment: false
  - id: D2
    description: "FAQ <summary> получает золотое focus-visible кольцо (добавлен в группу custom.css:351-358)"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: summary outline = 2px solid rgb(236,171,35) @1440"
        status: pass
    human_judgment: false
  - id: D3
    description: "FT1: тап-зона футер-ссылок ОБЕИХ колонок >=44px на 390/360"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: Разделы 26→44px, Услуги 46.5px @390/360 (getBoundingClientRect)"
        status: pass
    human_judgment: false
  - id: D4
    description: "F2: хит-зона .pfg-consent label >=44px"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: consent 36.375→44.38px @390, 62.56px @360"
        status: pass
    human_judgment: false
  - id: D5
    description: "CMP-06 модалки descoped — Magnific не инстанцирован, документация-маркер в CSS"
    requirement: "CMP-06"
    verification:
      - kind: other
        ref: "grep: pbmin-lightbox-video|pbmit-lightbox|magnificPopup|mfp- = 0 на 11 HTML; descope-комментарий present; pfg-modal = 0"
        status: pass
    human_judgment: false

# Metrics
duration: 18min
completed: 2026-06-26
status: complete
---

# Phase 3 Plan 02: FAQ-аккордеон + P1 тап-таргеты Summary

**Net-new FAQ через native `<details>/.pfg-faq` на services/contacts (клавиатура+ARIA из коробки, ноль связи с theme-handler), FT1/F2 тап-зоны подняты до WCAG 2.5.5 floor (44px) root-cause фиксом, CMP-06 честно descoped.**

## Performance

- **Duration:** ~18 min
- **Started:** 2026-06-26T13:36Z
- **Completed:** 2026-06-26T13:54Z
- **Tasks:** 3
- **Files modified:** 3 (services.html, contacts.html, css/custom.css)

## Accomplishments
- FAQ-аккордеон (CMP-05): 5 Q&A на services.html (услуги/цены/онбординг/сроки/документы) и 5 на contacts.html (связь/заявка/онбординг/ответ/документы); native `<details>` с классом `.pfg-faq` — клавиатура (Enter/Space), `[open]`-состояние и AT-семантика бесплатно, без JS; класс НЕ `.accordion` → theme-handler scripts.js:309 не перехватывает.
- FAQ стилизован токенами Фазы 2: collapsed/expanded/focus, золотой chevron с поворотом на `[open]`, summary >=16px (анти iOS-zoom); `<summary>` добавлен в focus-visible группу → золотое кольцо 2px #ecab23 (DOM-подтверждено); expand-переход chevron внесён в scoped reduced-motion блок.
- FT1 (AUD-02 P1) устранён по root-cause: DOM-измерение ОБЕИХ колонок до фикса показало, что 26px читает только «Разделы» (`.pbmit-footer-widget-col-2 .widget>ul.menu`, без two-column-обёртки), а «Услуги» уже 46.5px. Фикс — правило на общий предок `.site-footer .widget ul.menu li a` (padding 9+9px) → обе колонки 44px @390/360.
- F2 (AUD-02 P1) устранён: `.pfg-consent` min-height+padding → 36.375px @390 поднят до 44.38px (62.56px @360).
- CMP-06 модалки честно descoped: grep 0 триггеров Magnific на 11 HTML, документация-маркер (14.10) в CSS; модальная разметка/CSS/JS НЕ созданы.
- `js/custom.js` байт-идентичен (VER-04 сохранён); `!important` = 59 (net-new 0).

## Task Commits

1. **Task 1: FAQ markup net-new** - `48c0e80` (feat)
2. **Task 2: FAQ CSS + FT1/F2 тап-зоны** - `2bc07fd` (feat; включил и 14.10 descope-маркер Task 3)
3. **Task 3: CMP-06 descope** - зафиксирован в `2bc07fd` (комментарий 14.10), верифицирован grep=0

## Files Created/Modified
- `services.html` - FAQ `<section class="pfg-faq-section">` с 5 `<details class="pfg-faq-item">` перед `</main>`
- `contacts.html` - FAQ-секция с 5 `<details>` перед секцией формы
- `css/custom.css` - 14.7 (.pfg-faq стили + chevron), 14.8 (FT1 общий предок), 14.9 (F2 consent), 14.10 (CMP-06 descope-маркер); summary в focus-visible группе (стр.354); chevron в reduced-motion блоке (стр.386)

## Decisions Made
- **Native `<details>/<summary>` вместо button+region** (research A1, Claude's Discretion): браузер даёт фокусируемый summary, Enter/Space-тоггл, `[open]`-состояние и корректную AT-семантику бесплатно; класс `.pfg-faq` не матчит theme-handler `.accordion .accordion-item` (scripts.js:309) → нулевая интерференция.
- **initFaqA11y НЕ добавлен:** native `<details>` самодостаточен по клавиатуре и ARIA — JS-усилитель не нужен. `js/custom.js` остался байт-идентичным, что напрямую сохраняет VER-04 (форма→WhatsApp/меню/marquee не тронуты).
- **FT1 — общий предок, не углубление padding:** DOM-измерение подтвердило root-cause (промах селектора, не override) — старое правило 10.3 достаёт только `.pbmit-two-column-menu`. Новое правило целится в `.site-footer .widget ul.menu li a`, покрывая обе группы. CSS-only → footer markup не тронут → change-all-11 не триггерится.

## Deviations from Plan

None - plan executed exactly as written. CMP-06 descope-маркер (Task 3) физически вошёл в коммит Task 2, т.к. это один append-блок в custom.css; разделение на отдельный коммит создало бы пустую правку. Поведенчески все 3 задачи выполнены и верифицированы.

## Issues Encountered
- Счётчик `!important` подскочил до 62 из-за литеральной строки "без !important" в трёх русских комментариях (grep считает буквально). Переформулировал на «без important-флага» → вернулось к 59. Реальных деклараций `!important` не добавлено.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- FAQ, FT1, F2 готовы к полному phase-gate в плане 03-03 (DOM @5vp + axe + Lighthouse + VER-04 smoke по всем 11 страницам).
- Smoke на services/contacts @1440/390: no horizontal scroll, 0 JS-ошибок, FAQ=5 — theme JS не сломан.
- Не верифицировано в этом плане (зона 03-03): axe=0 и Lighthouse a11y>=95 на FAQ-страницах, полный VER-04 smoke (форма→WhatsApp клик), 3 промежуточных брейкпоинта (1024/768).

---
*Phase: 03-components*
*Completed: 2026-06-26*

## Self-Check: PASSED
- Files: services.html, contacts.html, css/custom.css, 03-02-SUMMARY.md — all FOUND
- Commits: 48c0e80, 2bc07fd — all FOUND
- !important count: 59 (<=59 budget)
