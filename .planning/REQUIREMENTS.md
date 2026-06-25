# Requirements: taxpfg.kz — Production UI Polish

**Defined:** 2026-06-25
**Core Value:** Сайт выглядит дорого, единообразно и убедительно на desktop/tablet/mobile, а conversion-блоки чисто конвертируют посетителя в лид — без изменения бизнес-логики.

## v1 Requirements

Требования текущего milestone. Каждое маппится на фазу roadmap. Audit-first: реализация только после утверждённого плана + UI design contract.

### Audit & Contract (deliverables-документы)

- [ ] **AUD-01**: Снять baseline (Lighthouse + axe-core, a11y/perf/CLS) по всем 11 страницам ДО любых правок — это «не хуже текущего» floor
- [ ] **AUD-02**: UI audit report — перечень визуальных проблем с привязкой «что/где/почему» по desktop/tablet/mobile
- [ ] **AUD-03**: Каталог конфликтов `custom.css` ↔ vendor-правила + список `!important` (текущая база ~59) и do-not-touch классов/атрибутов темы (`swiper-*`, `data-aos*`, `pbmit-*`)
- [ ] **AUD-04**: UI design contract — зафиксированные правила дизайна (токены, spacing scale, type scale, цвета+контраст, состояния, правила по компонентам, hard-constraints: visual-only, vendor read-only, no @layer, focus-always, scoped-motion)
- [ ] **AUD-05**: Implementation plan — какие файлы (`custom.css`/`base.css`/`custom.js`) менять и зачем, с порядком работ

### Design Tokens & Primitives

- [ ] **TOK-01**: Консолидировать дизайн-токены как CSS custom properties (палитра «чернила+золото», радиусы, тени, transitions, z-index) в `:root` слоя `custom.css` (грузится последним)
- [ ] **TOK-02**: Единый spacing scale на токенах, применённый к отступам секций/блоков — нет сломанных отступов
- [ ] **TOK-03**: Type scale: размеры заголовков/подзаголовков/body на `clamp()` (fluid), корректный line-height, читаемость; нет грубых переносов текста (`text-wrap: balance/pretty`, защита от orphans)

### Visual Hierarchy & Layout

- [ ] **VIS-01**: Единая визуальная иерархия — заголовки, подзаголовки, CTA, блоки, карточки выглядят системно на всех страницах
- [ ] **VIS-02**: Выравнивания и сетка приведены к единому spacing scale; нет визуального дрейфа между 11 страницами
- [ ] **VIS-03**: Цвета и контраст приведены к WCAG AA; золото не используется как body-текст там, где теряется контраст

### Components

- [ ] **CMP-01**: Кнопки — единая иерархия primary/secondary/ghost, состояния hover/focus/active/disabled, читаемый контраст
- [ ] **CMP-02**: Формы и инпуты — единый стиль, видимые labels, состояния focus/error/success, корректные мобильные клавиатуры; поведение формы→WhatsApp не меняется
- [ ] **CMP-03**: Карточки услуг — единый стиль, выравнивание, spacing, hover-состояние
- [ ] **CMP-04**: Навигация (sticky header + мобильное меню) — консистентный вид и состояния; theme-JS не ломается
- [ ] **CMP-05**: FAQ-аккордеон — корректная клавиатурная доступность и ARIA, единый вид
- [ ] **CMP-06**: Модалки (если используются Magnific Popup) — единый стиль и фокус-менеджмент

### Conversion Blocks

- [ ] **CNV-01**: Hero — чёткий value-prop, единственный заметный primary CTA, trust-сигналы выше сгиба
- [ ] **CNV-02**: Pricing/тарифы — понятная подача пакетов, выделение «популярного», ясное размещение CTA
- [ ] **CNV-03**: CTA по сайту — сильная визуальная иерархия, понятные, не перегруженные; разрешён конфликт sticky-mobile-CTA ↔ плавающая WhatsApp-кнопка
- [ ] **CNV-04**: Footer — единый, credibility-ориентированный вид, согласован на всех 11 страницах

### Imagery & Icons

- [ ] **IMG-01**: Изображения и иконки — единый стиль, корректные размеры, нет визуального мусора и искажений пропорций

### Accessibility

- [ ] **A11Y-01**: Видимый keyboard focus на всех интерактивных элементах (нет `outline:none` без замены)
- [ ] **A11Y-02**: ARIA где нужно (навигация, аккордеон, формы, модалки), читаемый текст, контраст AA
- [ ] **A11Y-03**: Анимации только в рамках scoped `prefers-reduced-motion`; новые движения не нарушают floor
- [ ] **A11Y-04**: Lighthouse/accessibility по всем страницам ≥ baseline (AUD-01) — не ухудшены

### Cross-Device Verification

- [ ] **VER-01**: Каждое изменение проверено на desktop/tablet/mobile (DOM-measured Playwright @ 1440/1024/768/390/360): мобильная версия не хуже десктопной
- [ ] **VER-02**: Финальный UI review со скриншотами и итоговым отчётом «до/после»
- [ ] **VER-03**: Список команд для локальной проверки (static server, Lighthouse, axe, Playwright-прогон)
- [ ] **VER-04**: Smoke-проверка: бизнес-логика, форма→WhatsApp, аналитика, роутинг, JSON-LD, анимации не затронуты

## v2 Requirements

Признано, но отложено за рамки текущего milestone.

### Performance / Payload

- **PERF-01**: Оптимизация изображений (WebP/AVIF, `srcset`, `loading=lazy`, `<picture>`) — ~6.9 МБ ассетов
- **PERF-02**: Удаление неиспользуемых vendor-библиотек (chart.js 208 КБ не подключён ни одной страницей)
- **PERF-03**: Оптимизация загрузки шрифтов (`font-display`, preload) против FOUT/FOIT/CLS

### Maintainability

- **MNT-01**: Механизм шаблонизации header/footer (устранить дублирование на 11 страниц) — потребовал бы build-систему

## Out of Scope

Явно исключено для предотвращения scope creep.

| Feature | Reason |
|---------|--------|
| Изменение бизнес-логики, API, платежей, аналитики, роутинга, user flows | Жёсткое ограничение заказчика |
| Правка vendor/theme-файлов (`bootstrap.min.css`, `style.css`, `responsive.css`, `shortcode.css`, `swiper.*`, `gsap*` и пр.) | Read-only ради обновляемости темы; правки только в `custom.css`/`base.css`/`custom.js` |
| CSS `@layer` для override темы | Vendor unlayered всегда побеждает layered → сломает каскад (research, HIGH) |
| Введение build-системы / бандлера / npm | Проект осознанно no-build; payload-оптимизация — отдельный milestone |
| Переписывание контента/копирайта | Не дизайн-задача |
| Смена CMS/бэкенда | Сайт остаётся статическим |

## Traceability

Заполняется при создании roadmap.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUD-01..05 | TBD | Pending |
| TOK-01..03 | TBD | Pending |
| VIS-01..03 | TBD | Pending |
| CMP-01..06 | TBD | Pending |
| CNV-01..04 | TBD | Pending |
| IMG-01 | TBD | Pending |
| A11Y-01..04 | TBD | Pending |
| VER-01..04 | TBD | Pending |

**Coverage:**
- v1 requirements: 28 total
- Mapped to phases: 0 (pending roadmap)
- Unmapped: 28 ⚠️

---
*Requirements defined: 2026-06-25*
*Last updated: 2026-06-25 after initial definition*
