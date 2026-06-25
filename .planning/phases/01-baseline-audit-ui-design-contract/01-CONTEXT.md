# Phase 1: Baseline Audit + UI Design Contract - Context

**Gathered:** 2026-06-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Эта фаза производит ДОКУМЕНТЫ, не правки кода (жёсткое audit-first требование заказчика). Делает четыре вещи:
1. Снимает регрессионный floor (Lighthouse + axe baseline по всем 11 страницам).
2. Перечисляет визуальные проблемы (что/где/почему) на desktop/tablet/mobile.
3. Каталогизирует конфликты `custom.css` ↔ vendor (`!important`-реестр + do-not-touch классы/атрибуты).
4. Фиксирует UI design contract (токены, spacing scale, type scale, цвет+контраст, состояния, hard-constraints) и implementation plan для последующих фаз.

Никаких изменений в `custom.css`/`base.css`/`custom.js` в этой фазе — только `.planning/`-артефакты.
</domain>

<decisions>
## Implementation Decisions

### Объём и инструментарий аудита (AUD-01, AUD-02)
- Baseline снимается двумя инструментами: Lighthouse + axe-core (Playwright-axe / axe DevTools) по всем 11 страницам.
- Визуальный аудит на 5 viewport-ах: 1440 / 1024 / 768 / 390 / 360, измерения DOM-measured через Playwright (верить измерению DOM, а не тексту CSS).
- Baseline-числа фиксируются таблицей per-page: a11y score, perf, CLS, LCP.
- Проблемы группируются по типам блоков (header/footer/hero/cards/forms — общие на всех 11 страницах), а не постранично, чтобы не дублировать одинаковые находки 11×.

### Spacing scale и type scale (TOK-02, TOK-03)
- Spacing scale: 4px-базовая шкала (4/8/12/16/24/32/48/64/96) как токены `--pfg-space-*`.
- Type scale: `clamp()` fluid, ratio ≈1.25 (major third), base body 16–18px, корректный line-height.
- Защита от переносов: `text-wrap: balance` на заголовках, `pretty` на body; non-breaking для русских предлогов/союзов.
- Привязка существующих значений: зафиксировать текущие отступы секций темы → ближайший токен шкалы, не ломая визуальный ритм (не полный пересчёт).

### Цвет, контраст и состояния компонентов (VIS-03, CMP-01…06, A11Y-02)
- Цветовые токены фиксируются как есть: ink `#16222d`, ink-deep `#0f1820`, gold `#ecab23`, gold-deep `#d6960f` (hover), gold-ink `#7a560a` (золотой текст на светлом, ≥5.4:1). Палитра НЕ расширяется.
- Контраст-флор: WCAG AA — текст ≥4.5:1, крупный/UI-элементы ≥3:1; золото как body-текст запрещено (только `gold-ink`).
- Обязательные состояния для всех интерактивных элементов: hover / focus-visible / active / disabled; focus всегда видим (нет `outline:none` без замены).
- Иерархия кнопок фиксируется контрактом: primary / secondary / ghost.

### Выходные документы фазы (AUD-03, AUD-04, AUD-05)
- Артефакты — отдельные секции/файлы под `.planning/phases/01-*/`: AUDIT (baseline+проблемы), CONFLICT-CATALOG, DESIGN-CONTRACT, IMPL-PLAN.
- Каталог конфликтов: перечислить `!important` (~59 baseline) + do-not-touch классы (`swiper-*`, `data-aos*`, `pbmit-*`) с привязкой к файлу/строке.
- Hard-constraints в контракте указываются явно: visual-only, vendor read-only, no `@layer`, focus-always, scoped-motion.
- Открытые вопросы из research решаются в этой фазе: live `<head>` font-loading config; инвентарь `<img>` vs CSS-background ассетов; какие страницы имеют pricing/FAQ/modal; остаётся ли удаление `chart.js` вне scope.

### Claude's Discretion
- Точный формат таблиц и внутренняя нумерация секций в артефактах.
- Какие именно страницы выбрать как репрезентативные при группировке проблем по типам блоков.
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `css/custom.css` (~951 строк) — премиальный слой «чернила+золото», грузится последним, ~59 `!important`. Уже содержит `--pfg-*` токены (`custom.css:284-302`), shadow/radius шкалы, easing `--pfg-ease`.
- `css/base.css` (~1166 строк) — vendor-токены `--pbmit-*` (`base.css:21-49`): brand-цвета, типографика, breakpoint. Источник истины brand-значений.
- `js/custom.js` (~201 строка) — IIFE с `initX()`-функциями (mobile menu, lead-form→WhatsApp, marquee fix, a11y-патчи).
- `.pfg-*` контентные примитивы: `.pfg-section`, `.pfg-card`, `.pfg-grid`, `.pfg-steps`, `.pfg-form`, `.pfg-lead`.

### Established Patterns
- Каскад-override: `custom.css` грузится последним и побеждает; `@layer` запрещён (vendor unlayered всегда бьёт layered).
- `!important` только для борьбы с vendor-правилами; новые `.pfg-*` элементы его не требуют.
- `prefers-reduced-motion` — scoped, не универсальный (гасит только декоративные микро-интеракции премиум-слоя, не brand-анимации Swiper/GSAP).
- Стиль комментариев в коде — русский, плотный, с обоснованием «почему» (vendor-поведение, замеренный контраст, WCAG-критерий).

### Integration Points
- Header/footer/nav/script-блок дублируются на всех 11 HTML — общие правки вносятся согласованно ×11 (нет include-механизма).
- Load order load-bearing: `custom.css` последний стиль, `custom.js` последний скрипт.
- Glass-header gated к `min-width:1201px` — decorative `filter`/`backdrop-filter`/`transform` нельзя вешать на предков мобильного off-canvas меню.

</code_context>

<specifics>
## Specific Ideas

- Известный target-size флаг в шапке темы ранее оставлен намеренно (память `ui-audit-2026-06-23.md`) — трогать только если попадёт в audit как блокер.
- Verify-каналы: Playwright (DOM-measured) + Chrome DevTools; цель a11y — 0 нарушений; верить DOM-измерению, а не тексту CSS (память `workflow-api-proxy-balance.md`).
- Предыдущий финальный аудит (Этап 10) — 6 правок только в `custom.css`/`custom.js`; известный target-size-флаг не чинен намеренно.

</specifics>

<deferred>
## Deferred Ideas

- PERF-01/02/03 (WebP/AVIF, удаление chart.js 208 КБ, font-display/preload) — v2, отдельный milestone.
- MNT-01 (шаблонизация header/footer) — потребовал бы build-систему, вне no-build ограничения.

</deferred>
