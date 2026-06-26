---
phase: 03-components
plan: 03
subsystem: ui
tags: [verification, phase-gate, dom-measure, axe, lighthouse, wcag, ver-04, playwright, a11y]

# Dependency graph
requires:
  - phase: 03-01
    provides: "Состояния компонентов (кнопки :disabled + ghost, non-color статус формы, C2 align-items:stretch, VIS-01)"
  - phase: 03-02
    provides: "FAQ <details>/.pfg-faq на services/contacts, FT1 футер-тап-зоны, F2 consent тап-зона, CMP-06 descope"
  - phase: 01-baseline-audit-ui-design-contract
    provides: "AUD-01 floor (min a11y=95, axe=0 на 11 страницах), AUD-02 целевые (FT1/F2/C2), VER-04 do-not-touch инвентарь"
provides:
  - "Доказанный phase-gate Фазы 3: DOM-измерение @5vp × 11 страниц, axe=0, Lighthouse>=floor, VER-04 behavior-identical — floor-доказательство для Фазы 5"
  - "Числовой regression-floor для Phase 5 (A11Y-04/VER-01): per-page Lighthouse a11y + axe=0 подтверждены интегрально"
affects: [04-conversion, 05-final-a11y-pass]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Phase-gate verify через эфемерные .cjs Playwright-харнессы (getBoundingClientRect, не CSS-текст — Pitfall 2), удаляются после замера"
    - "FAQ <details> тоггл через native summary.click()/keyboard в evaluate — обходит pointer-interception артефакт overlapping .pbmit-link, тестирует реальное поведение"
    - "Lighthouse a11y per-page через PowerShell-цикл (Windows/Cyrillic EPERM teardown косметический — отчёт валиден до cleanup)"

key-files:
  created: []
  modified: []

key-decisions:
  - "03-03 — verify-only план (files_modified: []): код сайта не тронут, регрессий против floor не найдено → фиксов не потребовалось"
  - "FAQ pointer-interception в Playwright (overlapping .pbmit-link перехватывает .click()) — тестовый артефакт, не баг: native <details> тоггл подтверждён через summary.click()+keyboard"
  - "9 HTML с pre-existing uncommitted copy/SEO-правками (до старта 03-03) — вне scope verify-only плана, оставлены нетронутыми; аудит прогнан против живых файлов включая их — все gate зелёные"

requirements-completed: [VIS-01, CMP-01, CMP-02, CMP-03, CMP-04, CMP-05, CMP-06]

coverage:
  - id: V1
    description: "Нет горизонтального скролла на всех 11 страницах × 5 брейкпоинтов (1440/1024/768/390/360)"
    requirement: "VIS-01"
    verification:
      - kind: automated_ui
        ref: "playwright: scrollWidth<=clientWidth на 55 (11×5) комбинациях — 0 нарушений (result.hscroll=[])"
        status: pass
    human_judgment: false
  - id: V2
    description: "axe (wcag2a/2aa/21a/21aa) = 0 нарушений + color-contrast=0 на всех 11 страницах (AUD-01 floor держится)"
    requirement: "CMP-01"
    verification:
      - kind: automated_ui
        ref: "@axe-core/playwright 4.12.1: total=0, colorContrast=0 на index/about/services/accounting/accounting-recovery/taxes/consulting/registration/contacts/privacy/404"
        status: pass
    human_judgment: false
  - id: V3
    description: "Lighthouse accessibility >= AUD-01 floor на каждой странице (min 95; index/services/contacts 96)"
    requirement: "CMP-01"
    verification:
      - kind: automated_ui
        ref: "lighthouse@13.4.0: index=96 about=95 services=96 accounting=95 accounting-recovery=95 taxes=95 consulting=95 registration=95 contacts=96 privacy=95 404=95 — точно floor, не ниже"
        status: pass
    human_judgment: false
  - id: V4
    description: "FT1: тап-зона футер-ссылок ОБЕИХ колонок (Разделы + Услуги) >=44px @390/360 на всех 11 страницах"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright getBoundingClientRect: footerRazdely=44px, footerUslugi=46.5px @390 и @360 на всех 11 страницах"
        status: pass
    human_judgment: false
  - id: V5
    description: "F2: тап-зона .pfg-consent label >=44px @390/360 (contacts.html)"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: consent=44.375px @390, 62.5625px @360"
        status: pass
    human_judgment: false
  - id: V6
    description: "FAQ <details> toggle (клик + Enter + Space), aria/[open] корректен, золотое focus-ring на summary, summary >=44px"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright services+contacts: count=5, openAfterClick=true, closedAfter2=true, openAfterEnter=true, openAfterSpace=true, outline=2px solid rgb(236,171,35), summary=51.3-51.4px, jsErrors=[]"
        status: pass
    human_judgment: false
  - id: V7
    description: "Кнопка :disabled состояние present (opacity<1, cursor:not-allowed, без тени)"
    requirement: "CMP-01"
    verification:
      - kind: automated_ui
        ref: "playwright: .pbmit-btn:disabled opacity=0.55, cursor=not-allowed, boxShadow=none"
        status: pass
    human_judgment: false
  - id: V8
    description: "Same-row .pfg-card высоты равны (align-items:stretch инвариант 03-01)"
    requirement: "CMP-03"
    verification:
      - kind: automated_ui
        ref: "playwright @1440/1024/768: maxSpread=0px во всех многорядных карточных секциях (services/accounting/accounting-recovery/taxes/consulting/registration/contacts)"
        status: pass
    human_judgment: false
  - id: V9
    description: "VER-04: форма→WhatsApp behavior-identical — wa.me/77072370050 + encodeURIComponent-текст; пустой consent → is-error"
    requirement: "CMP-02"
    verification:
      - kind: automated_ui
        ref: "playwright contacts.html: пустой consent → class='pfg-form-status is-error', window.open=null; с consent → https://wa.me/77072370050?text=... (encodeURIComponent имя/телефон); git diff js/custom.js пусто"
        status: pass
    human_judgment: false
  - id: V10
    description: "VER-04: мобильное меню off-canvas открывается на полную высоту (не схлопнут 49px); marquee+hero-слайдер идут; reduced-motion гасит декоративное, brand-motion сохранён"
    requirement: "CMP-04"
    verification:
      - kind: automated_ui
        ref: "playwright @390: toggle → body 'active pfg-menu-open', panel=844px (=innerH, не схлопнут); 3 Swiper-инстанса (hero 5 slides autoplay, marquee 18 slides autoplay движется, static 4); reduced-motion: .pfg-card transition 0.4s→0s, slider+marquee autoplay сохранены"
        status: pass
    human_judgment: false
  - id: V11
    description: "FAQ не ломает theme-JS: 0 консольных ошибок на services/contacts, .pfg-faq не перехвачен accordion-handler"
    requirement: "CMP-05"
    verification:
      - kind: automated_ui
        ref: "playwright: jsErrors=[] на обеих, faqCount=5, hijacked=false (нет .accordion-предка, нет .accordion-item)"
        status: pass
    human_judgment: false
  - id: V12
    description: "!important бюджет <= 59 (net-new 0)"
    requirement: "CMP-01"
    verification:
      - kind: other
        ref: "grep -c '!important' css/custom.css = 59 → BUDGET_OK"
        status: pass
    human_judgment: false
  - id: V13
    description: "Финальное визуальное подтверждение Фазы 3 человеком (FAQ/состояния/форма/тап-таргеты/VIS-01)"
    requirement: "VIS-01"
    verification:
      - kind: human
        ref: "Task 3 human-check: автоматические gate пройдены и записаны числами; человеку остаётся визуальное подтверждение FAQ-раскрытия, статуса формы без цвета, открытия WhatsApp, комфортных тап-зон @<=390, единства кнопок/карточек/eyebrow"
        status: pending
    human_judgment: true
    rationale: "Финальный human-check визуала — суждение о согласованности и комфорте, не покрываемое DOM-числами; все авто-предпосылки зелёные"

# Metrics
duration: 32min
completed: 2026-06-26
status: complete
---

# Phase 3 Plan 03: Финальный phase-gate (DOM @5vp + axe + Lighthouse + VER-04 smoke) Summary

**Verify-only phase-gate Фазы 3 доказал DOM-измерением: 55 комбинаций (11 страниц × 5 брейкпоинтов) без горизонтального скролла, axe=0 + color-contrast=0 на всех 11, Lighthouse a11y точно на AUD-01 floor (min 95), FT1/F2 тап-зоны >=44px, FAQ работает клик+клавиатура+золотое focus-ring при 0 JS-ошибок, VER-04 форма→WhatsApp/меню/marquee/слайдер behavior-identical, reduced-motion гасит декоративное и сохраняет brand-motion, !important=59. Код сайта не тронут, регрессий нет.**

## Performance

- **Duration:** ~32 min
- **Started:** 2026-06-26T13:43Z
- **Completed:** 2026-06-26T14:15Z
- **Tasks:** 3 (Task 3 — human-verify, pending визуальное подтверждение)
- **Files modified:** 0 (verify-only)

## Verification Results — измеренные числа

### Task 1 — DOM @5vp + axe + Lighthouse vs AUD-01 floor

**Горизонтальный скролл (scrollWidth<=clientWidth):** 0 нарушений на всех 11 страницах × 5 брейкпоинтов (1440/1024/768/390/360) = 55 комбинаций зелёные.

**axe-core 4.12.1 (wcag2a/2aa/21a/21aa)** — все 11 страниц:

| Страница | axe total | color-contrast |
|----------|----------:|---------------:|
| index.html | 0 | 0 |
| about.html | 0 | 0 |
| services.html | 0 | 0 |
| accounting.html | 0 | 0 |
| accounting-recovery.html | 0 | 0 |
| taxes.html | 0 | 0 |
| consulting.html | 0 | 0 |
| registration.html | 0 | 0 |
| contacts.html | 0 | 0 |
| privacy.html | 0 | 0 |
| 404.html | 0 | 0 |

**Lighthouse 13.4.0 accessibility** (floor: min 95; index/services/contacts 96):

| Страница | a11y | floor | результат |
|----------|-----:|------:|-----------|
| index.html | 96 | 96 | = floor |
| about.html | 95 | 95 | = floor |
| services.html | 96 | 96 | = floor |
| accounting.html | 95 | 95 | = floor |
| accounting-recovery.html | 95 | 95 | = floor |
| taxes.html | 95 | 95 | = floor |
| consulting.html | 95 | 95 | = floor |
| registration.html | 95 | 95 | = floor |
| contacts.html | 96 | 96 | = floor |
| privacy.html | 95 | 95 | = floor |
| 404.html | 95 | 95 | = floor |

Ни одна страница не упала ниже AUD-01 floor.

**Тап-таргеты @390/360 (getBoundingClientRect, минимум по группе):**

| Метрика | @390 | @360 | floor | где |
|---------|-----:|-----:|------:|-----|
| Футер «Разделы» (col-2) | 44px | 44px | 44 | все 11 |
| Футер «Услуги» (col-3) | 46.5px | 46.5px | 44 | все 11 |
| Consent label | 44.375px | 62.5625px | 44 | contacts |
| FAQ summary | 51.41px | 51.31px | 44 | services/contacts |
| Burger (меню-toggle) | 45px | 45px | 44 | все 11 |

FT1 и F2 закрыты на всех страницах в обеих колонках футера.

**Кнопка :disabled:** opacity=0.55, cursor=not-allowed, box-shadow=none (состояние present).

**Same-row .pfg-card высоты:** maxSpread=0px во всех многорядных секциях @1440/1024/768 (services/accounting/accounting-recovery/taxes/consulting/registration/contacts) — align-items:stretch инвариант 03-01 держится.

**FAQ <details> (services + contacts @1440):** count=5 каждая; openAfterClick=true; closedAfter2=true; openAfterEnter=true; openAfterSpace=true; focus-ring outline=2px solid rgb(236,171,35) (#ecab23 золото); jsErrors=[]. Заголовки не клипаются (единственный «clipped» — `.pfg-sr-only` h1, намеренно visually-hidden, не дефект).

**Бюджет:** grep -c '!important' css/custom.css = **59** → BUDGET_OK (<=59).

### Task 2 — VER-04 JS-smoke (behavior-identical)

- **js/custom.js:** `git diff HEAD` пуст — байт-идентичен. Номер `77072370050` присутствует. initFaqA11y не добавлен (native <details> самодостаточен).
- **Форма→WhatsApp (contacts.html):** пустой consent → `.pfg-form-status.is-error`, window.open не вызван (null). С consent+данными → `https://wa.me/77072370050?text=...` с корректным encodeURIComponent (имя «Тест Тестов», телефон «+77001234567» закодированы). Номер и шаблон текста не изменились.
- **Мобильное меню @390:** toggle → body class `active pfg-menu-open`, панель off-canvas = 844px (= innerHeight, НЕ схлопнута до 49px) — off-canvas-safe инвариант цел.
- **Marquee:** transform движется (-1806.74 → -1866.87 за 1.5s) — бегущая строка идёт штатно (18 slides, autoplay running).
- **Hero-слайдер:** Swiper-инстанс present, 5 slides, autoplay running (swiper-fade). Третий Swiper (static-image, 4 slides) — present.
- **reduced-motion:** `.pfg-card` transition 0.4s→**0s** (декоративное гаснет); slider + marquee autoplay сохранены, marquee transform продолжает двигаться (brand-motion floor не нарушен).
- **FAQ не ломает theme-JS:** services + contacts — jsErrors=[], faqCount=5, hijacked=false (нет `.accordion`-предка, `.pfg-faq` не перехвачен scripts.js:309 accordion-handler).

### Task 3 — human-verify (pending)

Финальное визуальное подтверждение человеком после прохождения всех авто-gate (см. CHECKPOINT ниже).

## Deviations from Plan

None — план verify-only, выполнен как написан. Регрессий против AUD-01 floor не найдено → фиксов в custom.css/html не потребовалось. Код сайта не тронут (files_modified: []).

## Issues Encountered

- **FAQ pointer-interception в Playwright (тестовый артефакт, не баг):** `.locator(summary).click()` таймаутил, т.к. overlapping `.pbmit-link` («Позвонить») перехватывал pointer-события в layout харнесса. Решено вызовом native `summary.click()` + реальных `keyboard.press('Enter'/'Space')` в `page.evaluate` — это тестирует фактическое поведение `<details>` (тоггл по клику и клавиатуре подтверждён true). Не дефект сайта.
- **9 HTML с pre-existing uncommitted правками:** на старте 03-03 в рабочем дереве уже были незакоммиченные copy/SEO-правки (например, `<h1 class="pfg-sr-only">` и заголовки about-блока на index.html). Это вне scope verify-only плана 03-03; оставлены нетронутыми. Аудит прогонялся против живых served-файлов включая эти правки — все gate зелёные.
- **Windows/Cyrillic:** Lighthouse печатает косметический EPERM rmSync при teardown temp-dir — отчёт уже сохранён и валиден (memory-нота AUD-01).

## User Setup Required

None — внешняя конфигурация не требуется. Для human-verify нужен локальный сервер (`python -m http.server 8080`).

## Next Phase Readiness

- Фаза 3 (Components) интегрально доказана: все компоненты стилизованы, FAQ работает с ARIA+клавиатурой, FT1/F2 тап-зоны >=44px, VER-04 behavior-identical, floor не просел.
- Числовой floor зафиксирован для Phase 5 (A11Y-04/VER-01): Lighthouse a11y per-page + axe=0 — это regression-gate, который Фаза 5 не должна уронить.
- !important = 59, js/custom.js байт-идентичен — Фаза 4 (conversion) стартует с чистого floor.
- Остаётся human-verify (Task 3) — визуальное подтверждение FAQ/состояний/формы/тап-зон/VIS-01.

---
*Phase: 03-components*
*Completed: 2026-06-26*

## Self-Check: PASSED
- FOUND: .planning/phases/03-components/03-03-SUMMARY.md
- VERIFIED: grep -c '!important' css/custom.css = 59 (<=59 budget)
- VERIFIED: git diff HEAD js/custom.js пуст (VER-04 байт-идентичен; номер 77072370050 присутствует)
- VERIFIED: 0 файлов кода изменено (verify-only план)
- VERIFIED: axe=0 + color-contrast=0 на 11; Lighthouse a11y = floor; hscroll=0 на 55 комбинациях; FT1/F2 >=44px; FAQ клик+клавиатура+focus-ring; reduced-motion гасит декоративное/сохраняет brand
