---
phase: 03-components
plan: 01
subsystem: ui
tags: [css, cascade-override, wcag, design-tokens, buttons, forms, cards, navigation, a11y]

# Dependency graph
requires:
  - phase: 02-tokens
    provides: "--pfg-* токены (цвета, тени, радиусы, spacing, easing) в :root, на которых строятся все состояния компонентов"
  - phase: 01-baseline-audit-ui-design-contract
    provides: "Component State Contract (CMP-01..04), AUD-02 находки (C2 height-jitter), VER-04 do-not-touch инвентарь"
provides:
  - "Кнопки .pbmit-btn: полная матрица состояний — добавлены :disabled и явный ghost-tier (.pfg-ghost) к существующим hover/focus-visible/active"
  - ".pfg-form-status: не-цветовая аффорданс (глиф ⚠/✓ + border-left + font-weight) поверх color-only — WCAG 1.4.1"
  - "C2 height-jitter диагностирован DOM-замером как cross-breakpoint reflow (не баг); .pfg-grid{align-items:stretch} как защитный инвариант"
  - "Документация nav-scope >=1201px glass-header + off-canvas-safe инвариант в custom.css"
  - "VIS-01: единый визуальный язык подтверждён grep'ом по 11 страницам (единые носители eyebrow/кнопок/карточек)"
affects: [04-conversion, 05-final-a11y-pass, 03-02-faq-footer-consent, 03-03-phase-gate-verify]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Cascade-override gap-fill: новые состояния через специфичность 0,2,0 + source-order (custom.css последний), net-new !important = 0"
    - "Diagnosis-before-fix: DOM-замер (Playwright getBoundingClientRect) ПЕРЕД наложением фикса, числа фиксируются в комментарии"
    - "Non-color affordance через ::before unicode-глиф (без иконочного шрифта, без сетевого запроса, не озвучивается AT)"

key-files:
  created: []
  modified:
    - "css/custom.css — новая секция «Этап 14 — состояния компонентов» (14.1–14.6)"

key-decisions:
  - "Ghost-tier как .pbmit-btn.pfg-ghost: прозрачный фон + --pfg-gold-ink текст + тонкая рамка; hover = мягкая золотая подложка rgba(.12), НЕ заливка (заливка = primary)"
  - "C2 — НЕ min-height-баг: same-row spread=0px на 1024/768/1440 (3 страницы); аудиторские 283 vs 256 = ожидаемый cross-breakpoint reflow; min-height не добавлен"
  - "Non-color статус через ⚠/✓ ::before + border-left 3px + font-weight 600 (избыточный сигнал поверх текста, который уже несёт смысл)"
  - "nav-scope: новых правил не добавлено — состояния навигации уже полны; раздел 14.4 — чистая enforcement-документация инварианта off-canvas"

patterns-established:
  - "Бюджет !important считается ЛИТЕРАЛЬНЫМ grep'ом — в комментариях избегать токена `!important`, формулировать «без форсирования каскада»"
  - "DOM-диагностика временными .cjs-скриптами в корне проекта (не в /tmp — там не резолвится локальный playwright), с последующей очисткой"

requirements-completed: [VIS-01, CMP-01, CMP-02, CMP-03, CMP-04]

coverage:
  - id: D1
    description: "Кнопки .pbmit-btn получили :disabled (opacity .55, cursor:not-allowed, box-shadow:none, подавлен hover-подъём) и явный ghost-tier (.pfg-ghost)"
    requirement: "CMP-01"
    verification:
      - kind: automated_ui
        ref: "playwright: getComputedStyle .pbmit-btn rest @1440 → box-shadow present, color #1b1b1b, text-transform none (present-state не регрессировал)"
        status: pass
      - kind: other
        ref: "grep css/custom.css → .pbmit-btn:disabled содержит opacity<1 + cursor:not-allowed + box-shadow:none; .pfg-ghost содержит background transparent + var(--pfg-gold-ink)"
        status: pass
    human_judgment: false
  - id: D2
    description: ".pfg-form-status.is-error/.is-ok несут не-цветовой признак (глиф ⚠/✓, border-left, font-weight) — различимы при цветовой слепоте"
    requirement: "CMP-02"
    verification:
      - kind: automated_ui
        ref: "playwright: contacts.html → is-error ::before content='⚠' borderLeft='3px solid' fontWeight=600; is-ok ::before content='✓' (оба состояния измерены)"
        status: pass
      - kind: other
        ref: "git diff --stat js/custom.js → пусто (VER-04 форма→WhatsApp байт-идентична)"
        status: pass
    human_judgment: false
  - id: D3
    description: "C2 height-jitter диагностирован: same-row .pfg-card высоты равны; добавлен .pfg-grid{align-items:stretch}"
    requirement: "CMP-03"
    verification:
      - kind: automated_ui
        ref: "playwright c2-measure: services/consulting/accounting-recovery @1024/768/1440 → same-row spread=0px везде (после правки повторно подтверждено)"
        status: pass
    human_judgment: false
  - id: D4
    description: "nav-scope >=1201px glass-header + off-canvas-safe инвариант задокументирован; состояния навигации подтверждены полными"
    requirement: "CMP-04"
    verification:
      - kind: other
        ref: "grep css/custom.css раздел 14.4 → фиксирует glass-scope >=1201px и запрет filter/transform/backdrop-filter на предках off-canvas"
        status: pass
    human_judgment: false
  - id: D5
    description: "VIS-01 единый визуальный язык подтверждён по 11 HTML"
    requirement: "VIS-01"
    verification:
      - kind: other
        ref: "grep -c по 11 HTML: единые носители .pbmit-subtitle (eyebrow), .pbmit-btn (CTA), .pfg-card (карточки) — нет per-page дивергентных классов"
        status: pass
    human_judgment: true
    rationale: "Единство «визуального языка» — суждение о согласованности рендеринга на всех страницах/брейкпойнтах; grep подтверждает носители классов, но финальная визуальная консистентность требует человеческого глаза (полный phase-gate в 03-03)"

# Metrics
duration: 18min
completed: 2026-06-26
status: complete
---

# Phase 3 Plan 01: Состояния компонентов (gap-fill) Summary

**Закрыты пробелы состояний кнопок (:disabled + ghost-tier), добавлена не-цветовая аффорданс статуса формы (WCAG 1.4.1), C2 height-jitter диагностирован DOM-замером как приемлемый reflow — всё через токены Фазы 2, net-new !important = 0**

## Performance

- **Duration:** ~18 min
- **Started:** 2026-06-26T13:21Z
- **Completed:** 2026-06-26T13:39Z
- **Tasks:** 3
- **Files modified:** 1 (css/custom.css)

## Accomplishments
- **CMP-01:** кнопки получили недостающее состояние `:disabled` (opacity .55, cursor:not-allowed, без тени, подавлен hover-подъём) и явный ghost-tier `.pbmit-btn.pfg-ghost` (прозрачный фон + `--pfg-gold-ink` текст + рамка; hover = мягкая золотая подложка, не заливка). Secondary-tier (`.white`/`.blackish`) задокументирован, не дублирован.
- **CMP-02:** `.pfg-form-status.is-error/.is-ok` получили не-цветовой признак состояния (префикс-глиф ⚠/✓ через `::before`, `border-left:3px`, `font-weight:600`) — состояние различимо без опоры на оттенок. `js/custom.js` не тронут (VER-04).
- **CMP-03:** C2 height-jitter диагностирован Playwright-замером ПЕРЕД фиксом — same-row spread = 0px на 1024/768/1440 (3 страницы). Подтверждено: это cross-breakpoint reflow, не min-height-баг. Добавлен защитный `.pfg-grid{align-items:stretch}`.
- **CMP-04:** задокументирован nav glass-scope `>=1201px` + off-canvas-safe инвариант; состояния навигации уже полны — новых правил не потребовалось.
- **VIS-01:** единый визуальный язык подтверждён grep'ом по 11 HTML (единые носители eyebrow/кнопок/карточек, палитра заморожена).

## Task Commits

Each task was committed atomically:

1. **Task 1: Кнопки — :disabled + ghost-tier (CMP-01)** - `3828883` (feat)
2. **Task 2: Форма — non-color affordance + nav-scope doc (CMP-02, CMP-04)** - `ffb2cd2` (feat)
3. **Task 3: Карточки — диагностика C2 + VIS-01 enforcement (CMP-03, VIS-01)** - `b1fd70d` (feat)

## Files Created/Modified
- `css/custom.css` - добавлена секция «Этап 14 — состояния компонентов» (подразделы 14.1 кнопки:disabled, 14.2 ghost-tier, 14.3 non-color статус формы, 14.4 nav-scope doc, 14.5 C2-диагностика + align-items:stretch, 14.6 VIS-01 enforcement). +156 строк.

## Decisions Made
- **Ghost hover = подложка, не заливка:** золотая заливка зарезервирована за primary-tier; ghost на hover получает `rgba(236,171,35,.12)` подложку + углубление текста до `--pfg-gold-deep`, чтобы иерархия CTA читалась.
- **C2: min-height НЕ добавлен.** DOM-замер показал spread=0px в каждом ряду на всех ширинах. Жёсткий min-height сломал бы естественный reflow. Добавлен только явный `align-items:stretch` как защита инварианта.
- **Non-color глиф через unicode `::before`** (⚠ \26A0 / ✓ \2713) вместо иконочного шрифта — без сетевого запроса, не озвучивается AT (текст статуса остаётся семантическим носителем).
- **nav 14.4 — документация, не правила:** состояния навигации (underline-grow, focus-ring, тап-таргеты) уже полны; раздел фиксирует off-canvas-safe инвариант для будущих правок.

## Deviations from Plan

None - plan executed exactly as written. (Все 3 задачи выполнены по acceptance_criteria; никаких Rule 1-4 отклонений не потребовалось.)

## Issues Encountered
- **Бюджет !important ложно превышал 59** после Task 1 и Task 3: метрика — литеральный `grep -c '!important'`, и слово `!important` в русских комментариях попадало в счёт. Решено переформулировкой комментариев («без форсирования каскада» / «net-new important-флагов») — фактических `!important`-деклараций не добавлено, бюджет остался 59. Зафиксировано как паттерн.
- **Временные Playwright-скрипты не резолвят `playwright` из `/tmp`** (Windows, локальный node_modules). Скрипты писались в корень проекта и удалены после замеров.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Кнопочная иерархия (primary/secondary/ghost × 4 состояния) готова к использованию в Фазе 4 (conversion CTA).
- `.pfg-ghost` зарегистрирован в CSS, но в разметку ещё не введён — это намеренно (доступный tier для Фазы 4).
- Планы 03-02 (FAQ-аккордеон, FT1 footer hit-zone, F2 consent) и 03-03 (полный phase-gate: DOM @5vp + axe + Lighthouse + VER-04 smoke) — следующие волны фазы 03.
- Бюджет !important = 59 (floor держится), js/custom.js не тронут.

---
*Phase: 03-components*
*Completed: 2026-06-26*
## Self-Check: PASSED
- FOUND: .planning/phases/03-components/03-01-SUMMARY.md
- FOUND: commits 3828883, ffb2cd2, b1fd70d
- FOUND: css/custom.css «Этап 14» section (14.1–14.6)
- VERIFIED: !important budget = 59 (no net-new); git diff js/custom.js empty (VER-04)
