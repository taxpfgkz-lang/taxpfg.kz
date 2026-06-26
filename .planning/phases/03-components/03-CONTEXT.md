# Phase 3: Components - Context

**Gathered:** 2026-06-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Стилизует все переиспользуемые компоненты системно (со всеми состояниями), чтобы единый вид дошёл до 11 страниц через токен-слой Фазы 2. Правки в `css/custom.css` (первично), `js/custom.js` (a11y/ARIA-слой), и **HTML страниц** (markup-scope расширен Юрием 2026-06-26 — см. STATE/memory). Требования: VIS-01, CMP-01…CMP-06.

Зависит от Фазы 2: компоненты стилизуются токенами spacing/type/color, не хардкодом.
</domain>

<decisions>
## Implementation Decisions

### Net-new компоненты (CMP-05 FAQ, CMP-06 модалки)
- CMP-05 FAQ-аккордеон — построить ПОЛНОСТЬЮ: HTML `.accordion`-разметка (theme-handler js/scripts.js:309 уже существует, но ни одна страница не инстанцирует) + корректный ARIA + клавиатура. Разместить на **services.html** (вопросы об услугах) и **contacts.html** (перед формой) — типовые конверсионные места.
- FAQ a11y-слой — в js/custom.js (ARIA-состояния expanded/collapsed, keyboard) поверх theme-handler, по существующему initX()-паттерну (guard + early-return + idempotent). Форма→WhatsApp behavior-identical.
- CMP-06 модалки — **DESCOPE**: Magnific Popup загружен на 11 страницах, но триггеров (.pbmin-lightbox-video / a.pbmit-lightbox) ноль. Контракт гейтит «только если инстанцирован». НЕ фабриковать модалку. Зафиксировать descope честно.

### Стилизация существующих компонентов (CMP-01/02/03/04)
- Кнопки (CMP-01): primary/secondary/ghost через override `.pbmit-btn` (не переименовывать), все 4 состояния hover/focus-visible/active/disabled. Primary=gold fill #ecab23 + ink-текст AA; secondary=outline/ink; ghost=text-weight + gold-ink hover. Тени --pfg-shadow-btn/-btn-h.
- Формы (CMP-02): rest/focus/error/success на `.pfg-form .form-control`; error/success через `.pfg-form-status` + классы. Soft gold focus-ring. Форма→WhatsApp поведение НЕ меняется.
- Карточки (CMP-03): rest + hover-lift (декоративный → в scoped reduced-motion блок custom.css:332-345); выровнять height-jitter (C2: 283px@1024 vs 256px@768).
- Навигация (CMP-04): rest/hover-underline-grow/active/focus-visible; glass-header gated ≥1201px; off-canvas-safe (нет filter/transform/backdrop-filter на предках мобильного меню). Theme-JS не ломать.

### a11y/tap-target markup-фиксы (AUD-02 P1)
- FT1 footer links 26px (P1): починить 44px hit-zone через CSS padding на footer nav-links — выяснить, почему текущее правило custom.css:565-571 не применяется к этой группе ссылок (DOM-vs-CSS расхождение). Shared chrome → change-all-11 если трогается markup.
- F2 consent label 36px (P1): поднять hit-area до ≥44px через CSS (padding/min-height на `.pfg-consent label`).
- Подход: CSS-only где достигает (FT1/F2 — это padding/min-height); markup только если CSS не достаёт.
- VIS-01: свести heading/subheading/CTA/блоки/карточки к одному визуальному языку через токены Фазы 2 на всех 11 страницах.

### change-all-11 дисциплина и verify
- Shared chrome (header/footer/nav) — любая markup-правка атомарно во все 11 HTML (grep возвращает 11), один коммит.
- FAQ не shared (разный контент на services/contacts) → единый СТИЛЬ без change-all-11 на контент.
- !important бюджет: net-new ≈ 0 (floor 59); каждый новый — с русским комментарием о перебиваемом vendor-правиле.
- Verify: Playwright DOM-measured @ 1440/1024/768/390/360 + axe + VER-04 JS-smoke (форма→WhatsApp/меню/marquee/slider/reduced-motion) против AUD-01 floor (a11y≥95, axe=0).

### Claude's Discretion
- Точные значения паддингов/теней состояний (в рамках токенов и контракта).
- Конкретный HTML-каркас FAQ-аккордеона (semantic <details>/<summary> vs button+region) — выбрать по лучшей a11y и совместимости с theme-handler.
- Сколько FAQ-вопросов и их формулировки (контент) — разумный минимум для услуг.
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Токены Фазы 2 в :root custom.css (--pfg-space-*, --pfg-fs-*/--pfg-lh-*, --pfg-z-float) — компоненты стилизуются ими.
- `.pbmit-btn` — theme-кнопка (override, не переименовывать). Focus-ring reference: outline:2px solid var(--pfg-gold);outline-offset:3px (custom.css:307-314).
- `.pfg-form` / `.form-control` (contacts.html — единственная форма), `.pfg-form-status` (role=status aria-live), `.pfg-consent` label, `.pfg-card`, `.site-footer`.
- FAQ theme-handler: js/scripts.js:309 (существует, не инстанцирован).
- js/custom.js initX()-паттерн: IIFE, DOMContentLoaded, guard+early-return, idempotent-патчи; initSvgAria/initSearchA11y — образцы a11y-патчей.

### Established Patterns
- prefers-reduced-motion scoped (custom.css:332-345) — декоративные lift/underline сюда; brand-motion (Swiper/marquee/GSAP/AOS) не трогать.
- text-transform:none на русском там, где тема навязывает capitalize/uppercase.
- 44px hit-zone (WCAG 2.5.5) на интерактивных глифах (custom.css:164-170, footer :565-571 — но FT1 показывает что к footer-links не применяется).

### Integration Points
- Glass-header gated ≥1201px; off-canvas-safe constraint (нет filter/transform на предках off-canvas меню).
- Shared chrome (header/footer/nav/scripts) дублируется ×11 — change-all-11.
- custom.css последний стиль, custom.js последний скрипт.

### AUD-02 component findings Phase 3 lands
- C1 card padding 28px (уже снапнут в Фазе 2 — проверить) / C2 height-jitter.
- F1 input 15px (уже починен Фазой 2 — 16px) / F2 consent label 36px (P1, чинить).
- FT1 footer links 26px (P1, чинить 44px). N1/N2 nav tap-targets здоровы (документировать ≥1201 scope).
</code_context>

<specifics>
## Specific Ideas

- Источники: 01-UI-SPEC.md Component State Contract + Hard Constraints; 01-AUDIT.md AUD-02 (C2/F2/FT1 + positive findings); 01-IMPLEMENTATION.md Phase 3 file-map; 01-CONFLICT-CATALOG.md (do-not-touch, 59 budget).
- Markup-scope расширен (Юрий 2026-06-26): HTML editable широко. VER-04 поведение и vendor-read-only остаются жёсткими.
- Verify durable channel: python -m http.server + Playwright DOM @5vp + npx axe. Верить DOM, не CSS-тексту.

</specifics>

<deferred>
## Deferred Ideas

- CMP-06 модалки — descoped (Magnific не инстанцирован); если позже инстанцируют — отдельная задача.
- Conversion-блоки (hero/pricing CNV-02/CTA/footer) — Phase 4.
- Финальный a11y pass + cross-device verification + before/after — Phase 5.
- PERF (image/font опт), MNT (templating) — v2.

</deferred>
