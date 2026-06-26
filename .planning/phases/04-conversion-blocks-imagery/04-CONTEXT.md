# Phase 4: Conversion Blocks + Imagery - Context

**Gathered:** 2026-06-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Конверсионные композиты конвертируют чисто, imagery консистентна — на стабильных компонентах Фазы 3. Правки: `css/custom.css` (первично), HTML страниц (pricing net-new, footer-паритет), `js/custom.js` (только если реально нужно — см. CNV-03). Требования: CNV-01, CNV-02, CNV-03, CNV-04, IMG-01.

Зависит от Фазы 3: conversion-блоки — композиты кнопок/карточек/форм Фазы 3.
</domain>

<decisions>
## Implementation Decisions

### Pricing-блок CNV-02 (net-new, на сайте отсутствует)
- Разместить на **services.html** (после hero/услуг, перед FAQ) — единственное логичное место.
- Структура: 3 пакета (напр. ИП-старт / ТОО-стандарт / Премиум), ровно один «популярный» highlight, per-tier CTA.
- Контент цен: БЕЗ конкретных цифр — формулировки про объём услуг; цена «от X ₸» или «по запросу» → CTA. (Точные цены не задавать — риск устаревания, бизнес не подтвердил тарифы.)
- CTA тарифа → тот же WhatsApp-flow (паттерн «Получить консультацию», VER-04 — не новая логика, переиспользовать существующий механизм формы/ссылки).
- pricing — page-specific (только services.html) → НЕ shared chrome → НЕ change-all-11.

### Hero + sticky-CTA коллизия (CNV-01, CNV-03)
- Hero CNV-01: полировать существующий — value-prop + единственный primary CTA + trust-сигналы выше сгиба; чинит HE1/HE2 (hero line-height; height/LCP — visual, perf не gate).
- **Sticky mobile CTA НЕ существует на сайте** (grep подтвердил). CNV-03 коллизия sticky-CTA↔WhatsApp-float физически отсутствует.
- CNV-03 разрешение: НЕ создавать net-new sticky-CTA. Задокументировать: sticky-CTA отсутствует → коллизии нет; `.pfg-whatsapp-float` (js/custom.js:58-60) — единственный плавающий элемент, ничего не перекрывает. Это удовлетворение CNV-03 через отсутствие конфликта, честно зафиксировать. JS-правки в этой фазе НЕ требуются (CNV-03 был единственным JS-кандидатом).
- CTA-иерархия по сайту: единая через токены/компоненты Фазы 3 (один заметный primary на экран).

### Footer-паритет + imagery (CNV-04, IMG-01)
- Footer CNV-04: унифицировать вид на 11/11 (footer присутствует везде); FT3 vertical density на mobile (low-priority). Если markup трогается — change-all-11 атомарно.
- IMG-01: presentation/sizing ONLY (object-fit, корректные пропорции, нет искажений/визуального мусора) на существующие 12 `<img>` + CSS-bg. WebP/AVIF/srcset bulk re-encode = v2/PERF-01 OUT-OF-SCOPE.
- T1 title-bar: добавить min-height tier между 768 и 390 (550px band fix на 768).

### change-all-11 дисциплина и verify
- Footer markup-правки — атомарно во все 11 HTML (grep=11), один коммит.
- Pricing — только services.html → не change-all-11.
- !important бюджет: net-new ≈ 0 (floor 59); каждый новый — с русским комментарием о vendor-правиле.
- Verify: Playwright DOM @ 1440/1024/768/390/360 + axe + VER-04 JS-smoke против AUD-01 floor (a11y≥95, axe=0); pricing CTA→WhatsApp работает (тот же flow); footer-паритет на 11.

### Claude's Discretion
- Точные названия/состав 3 тарифов и формулировки (русский sentence case, осмысленно для бухгалтерско-налоговых услуг).
- Какие trust-сигналы поднять в hero выше сгиба (из существующего контента).
- Конкретные object-fit/sizing значения для imagery.
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Компоненты Фазы 3: .pbmit-btn (primary/secondary/ghost +4 состояния), .pfg-card, .pfg-form, .pfg-faq — pricing-блок композирует из них.
- Токены Фазы 2 (--pfg-space-*, --pfg-fs-*/lh-*, gold/ink) — pricing/hero стилизуются ими.
- `.pfg-whatsapp-float` (js/custom.js:58-60) — единственный sticky/floating элемент.
- Hero: .pbmit-slider-title (index.html:169/200/231 — 3 слайда), уже с line-height policy Фазы 2.
- Footer .site-footer на 11/11; gold top-border 3px (FT2 positive).

### Established Patterns
- Форма→WhatsApp: initLeadForm (js/custom.js:72-111), wa.me/77072370050 + encodeURIComponent — pricing CTA переиспользует этот flow, НЕ новый.
- scoped reduced-motion (custom.css ~376-389) — декоративные hover на pricing-картах сюда.
- text-transform:none на русском.

### Integration Points
- Shared chrome (footer/header/nav) дублируется ×11 → change-all-11.
- Pricing на services.html — page-specific.
- custom.css последний; off-canvas-safe; no @layer.

### AUD-02 findings Phase 4 lands
- HE1/HE2 hero line-height (lh policy уже Фаза 2) + height/LCP polish (visual).
- T1 title-bar 550px band на 768 → min-height tier 768→390.
- I1/I2 imagery sizing (presentation only; re-encode v2).
- FT3 footer vertical density mobile (low-priority).

</code_context>

<specifics>
## Specific Ideas

- Источники: 01-UI-SPEC.md (accent reserved-for list включает «единственный популярный pricing-tier highlight»), 01-AUDIT.md (HE/T1/I/FT3), 01-IMPLEMENTATION.md Phase 4 file-map, 01-CONFLICT-CATALOG (59 budget, do-not-touch).
- Markup-scope расширен (Юрий) — HTML editable; vendor read-only + VER-04 жёсткие.
- Verify durable: python http.server + Playwright DOM @5vp + axe. Верить DOM.
- ВАЖНО: imp-plan предполагал sticky-CTA коллизию (CNV-03 JS-спайк), но sticky-CTA НЕ существует — CNV-03 решается документированием отсутствия коллизии, без JS. Это снимает единственную JS-задачу фазы.

</specifics>

<deferred>
## Deferred Ideas

- WebP/AVIF/srcset image re-encode — v2/PERF-01.
- Точные цены тарифов — ждут подтверждения бизнеса (пока «по запросу»).
- Финальный a11y pass + cross-device verification + before/after — Phase 5.
- chart.js removal, font-loading opt, header/footer templating — v2.

</deferred>
