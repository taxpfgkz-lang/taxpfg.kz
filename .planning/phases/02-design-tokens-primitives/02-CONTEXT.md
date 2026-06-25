# Phase 2: Design Tokens + Primitives - Context

**Gathered:** 2026-06-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Первая фаза, реально меняющая код (`css/custom.css`, при необходимости `css/base.css`; `js/custom.js` НЕ трогается). Закладывает единый токен-фундамент, который наследует всё downstream:
1. Консолидированный `:root` `--pfg-*` токен-лист (ink+gold палитра, radii, shadows, transitions, z-index) — TOK-01.
2. 4px spacing scale `--pfg-space-*`, применённая точечно к отступам секций/блоков — TOK-02, VIS-02.
3. Fluid `clamp()` type scale (ratio ≈1.25) с корректным line-height и русскими правилами переноса — TOK-03.
4. Контраст WCAG AA: gold-текст только через `--pfg-gold-ink`, gold-fill не как body-текст — VIS-03.

Это root-зависимость: компоненты (Phase 3) и conversion-блоки (Phase 4) не композируются, пока токены/scales не приземлятся. `custom.css` остаётся последним в load order (побеждает по source-order).
</domain>

<decisions>
## Implementation Decisions

### Стратегия применения spacing scale (TOK-02, VIS-02)
- Объявить `--pfg-space-*` (4/8/12/16/24/32/48/64/96) + точечно заменить отступы по AUD-02-находкам (card 28px → `--pfg-space-6`/`-8`, rhythm-snap по section paddings). НЕ переписывать корректно читающиеся отступы.
- Замена существующих значений = snap к ближайшему токену, сохраняя визуальный ритм темы (не точные значения шкалы везде).
- VIS-02 (выравнивание/сетка): чинить только задокументированный в AUD-02 дрейф; НЕ реструктурировать vendor-grid.

### Fluid type scale + переносы (TOK-03)
- `clamp()` по ролям UI-SPEC (body / label / heading / display), ratio ≈1.25; чинит AUD-02 HE1/T2/G2 (heading line-height < font-size).
- Русские переносы: `text-wrap: balance` на заголовках, `pretty` на body + non-breaking для коротких предлогов/союзов (в, и, с, к, на, по, от).
- iOS focus-zoom (AUD-02 F1): mobile input font-size 15px → ≥16px через scale/токен.
- Объявление scale в `:root` слоя `custom.css` (грузится последним, побеждает), НЕ через base.css.

### Дисциплина токенов и !important-бюджет (TOK-01, VIS-03)
- Свести ink+gold/radii/shadows/transitions/z-index в один `:root`-лист, переиспользуя `--pbmit-*` через `var()` (палитра НЕ расширяется новыми цветами).
- `!important`-бюджет: net-new ≈ 0 (floor = 57 функциональных деклараций из 01-CONFLICT-CATALOG). Каждый новый `!important` — с русским комментарием о перебиваемом vendor-правиле. 31 из 57 существующих uncited — подтвердить фактический beaten-селектор перед relocate/drop.
- VIS-03: gold-текст только `--pfg-gold-ink` (#7a560a, ≥5.4:1); gold-fill #ecab23 не трогать.
- `base.css` правки только если необходимо сослаться/хирургически переопределить `--pbmit-*` (namespace base.css:21-49); по умолчанию читать vendor-токен через `var()` из custom.css.
- Никакого `@layer` (unlayered vendor всегда бьёт layered) — побеждать source-order + точечной специфичностью.

### Claude's Discretion
- Точная организация/порядок токенов внутри `:root`-листа.
- Конкретные clamp() min/max значения для каждой роли (в рамках ratio 1.25, base body 16–18px).
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `css/custom.css` (~951 строк, грузится последним, 57 функциональных !important): уже содержит `--pfg-*` токены (`custom.css:284-302`), shadow/radius шкалы, easing `--pfg-ease`, `--pfg-gold-ink` для контраста. Phase 2 консолидирует и расширяет это.
- `css/base.css:21-49`: vendor `--pbmit-*` токены (brand color/typography, body line-height `--pbmit-body-typography-line-height`, btn font-size 15px, body 17px). Источник истины brand-значений.
- `.pfg-*` примитивы: `.pfg-section`, `.pfg-card`, `.pfg-grid`, `.pfg-prose` — получат токен-based отступы.

### Established Patterns
- prefers-reduced-motion — scoped (custom.css:332-345), гасит только декоративные микро-интеракции; brand-анимации (Swiper/GSAP) не трогать.
- `text-transform: none` на русском тексте там, где тема навязывает capitalize/uppercase (custom.css:215-218, :243-258, :865-873).
- Tap-target 44px hit-zone (WCAG 2.5.5) на интерактивных глифах (custom.css:164-170).

### Integration Points
- Glass-header gated к min-width:1201px — decorative filter/backdrop-filter/transform нельзя на предков мобильного off-canvas меню.
- Load order load-bearing: custom.css последний стиль.
- 11 HTML дублируют chrome — но Phase 2 = чистый CSS-токен слой, markup не трогается, так что change-all-11 здесь не возникает.

### AUD-02 findings Phase 2 lands
- HE1/T2/G2: heading line-height < font-size (hero 170/150px) → нормализовать через clamp + lh policy.
- C1: card padding 28px → snap `--pfg-space-6`/`-8`.
- F1: mobile input font-size 15px → ≥16px (iOS focus-zoom).
- Title-bar 550px persisting на 768px tablet (P2) — частично spacing, рассмотреть.

</code_context>

<specifics>
## Specific Ideas

- Источники истины для Phase 2: 01-CONFLICT-CATALOG.md (57 !important + do-not-touch), 01-AUDIT.md (AUD-02 visual problems с DOM-измерениями), 01-UI-SPEC.md (контракт токенов/scales/color), 01-IMPLEMENTATION.md (Phase 2 file-change order).
- Verify-канал (durable, подтверждён Юрием): Playwright DOM-measured @ 1440/1024/768/390/360 + axe против AUD-01 floor (a11y≥95, axe=0). Верить DOM-замеру, не тексту CSS.
- JS smoke (VER-04): меню / WhatsApp float / lead-form→WhatsApp / marquee / slider / reduced-motion должны остаться behavior-identical.

</specifics>

<deferred>
## Deferred Ideas

- Компоненты (кнопки/формы/карточки состояния) — Phase 3, после приземления токенов.
- Conversion-блоки + imagery — Phase 4.
- Финальная a11y + cross-device verification против floor — Phase 5.
- PERF-01/02/03, MNT-01 — v2.

</deferred>
