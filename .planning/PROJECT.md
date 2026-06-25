# taxpfg.kz — Production UI Polish

## What This Is

taxpfg.kz — статический сайт-визитка бухгалтерско-налоговой консалтинговой фирмы (PrimeFinance Group) в Казахстане. 11 HTML-страниц на базе коммерческой темы GudFin (PBMIT) с наложенным премиальным слоем «чернила + золото» (`css/custom.css`, `css/base.css`, `js/custom.js`). Цель текущего milestone — провести полный UI-аудит и довести визуал до production-уровня, не трогая бизнес-логику, формы и user flows.

## Core Value

Сайт должен выглядеть дорого, единообразно и убедительно на desktop/tablet/mobile, а ключевые conversion-блоки (hero, тарифы, формы, CTA) — чисто конвертировать посетителя в лид. Если всё остальное провалится — это должно работать.

## Business Context

- **Customer**: МСБ Казахстана, ищущий аутсорс бухгалтерии/налогов; посетитель сайта → лид через форму/WhatsApp
- **Revenue model**: лидогенерация (заявки на бухгалтерские/консалтинговые услуги)
- **Success metric**: конверсия посетитель→заявка; визуальное доверие к бренду
- **Strategy notes**: лид-форма уводит в WhatsApp (`js/custom.js`)

## Requirements

### Validated

<!-- Выведено из существующего кода (.planning/codebase/) — это уже работает и не должно сломаться. -->

- ✓ **Phase 1 (2026-06-25):** Baseline floor снят (Lighthouse a11y 95-96, axe 0 нарушений ×11) + UI design contract + conflict catalog + implementation plan зафиксированы (AUD-01..05) — validated
- ✓ 11 статических HTML-страниц с уникальными meta/SEO и JSON-LD `AccountingService` — existing
- ✓ Премиальный слой «чернила+золото» поверх темы GudFin (`css/custom.css` загружается последним) — existing
- ✓ Лид-форма с уводом в WhatsApp (`js/custom.js`) — existing
- ✓ Мобильное меню, бегущая строка услуг, маркиз-тюнинг (`js/custom.js`) — existing
- ✓ Пройден a11y/визуальный рефакторинг: единые отступы секций, `prefers-reduced-motion`, a11y-фиксы (коммиты c08cbd3, 830a769) — existing
- ✓ Адаптивная вёрстка на Bootstrap 5.2 + `css/responsive.css` — existing

### Active

<!-- Текущий milestone: Production UI Polish. Audit-first, изменения только после утверждённого плана + UI design contract. -->

<!-- Phase 1 завершена 2026-06-25: baseline-аудит + UI design contract зафиксированы (AUD-01..05). -->

- [ ] Визуальная иерархия: заголовки, подзаголовки, CTA, блоки, карточки — единообразны
- [ ] Выравнивания, отступы, сетка, единый spacing scale
- [ ] Типографика: размеры, line-height, переносы, читаемость; нет грубых переносов текста
- [ ] Цвета и контраст; состояния hover/focus/active/disabled для интерактивных элементов
- [ ] Компоненты: кнопки, формы, инпуты, карточки, модалки, навигация — консистентны
- [ ] Адаптивность: mobile не хуже desktop; нет сломанных отступов и переносов
- [ ] Conversion-блоки: hero, тарифы/pricing, FAQ, footer, CTA — визуально сильные и понятные
- [ ] Изображения/иконки: единый стиль, корректные размеры, нет визуального мусора
- [ ] Accessibility: keyboard focus, aria где нужно, контраст, читаемый текст; Lighthouse/a11y не хуже текущего
- [ ] Финальный UI review со скриншотами и списком команд локальной проверки

### Out of Scope

- Изменение бизнес-логики, API, платежей, аналитики, роутинга, существующих user flows — **жёсткое ограничение заказчика**
- Правка vendor/theme-файлов (`bootstrap.min.css`, `style.css`, `responsive.css`, `shortcode.css`, `swiper.*`, `gsap*`, `chart.js` и пр.) — read-only, чтобы тему можно было обновлять; все правки только в `custom.css`/`base.css`/`custom.js`
- Введение build-системы / бандлера / npm — проект осознанно остаётся no-build (можно отметить как отдельный будущий milestone)
- Переписывание контента/копирайта страниц — не дизайн-задача
- Смена CMS/бэкенда — сайт остаётся чисто статическим
- Известный target-size флаг в шапке темы — ранее оставлен намеренно (см. память проекта); трогаем только если попадёт в audit как блокер

## Context

- **Стек:** чистый статический HTML5/CSS3/ES5-JS, без сборки и backend. Vendor-библиотеки вкоммичены (Bootstrap 5.2, jQuery 3.7, Swiper 7.3, GSAP 3.10, AOS, Magnific Popup, Chart.js 4.5). Подробно — `.planning/codebase/STACK.md`.
- **Кастомный слой:** правки только в `css/custom.css` (~951 строк, `!important` ~59×, грузится последним), `css/base.css` (~1166 строк), `js/custom.js` (~201 строка). Всё остальное под `css/` и `js/` — read-only.
- **Архитектура:** см. `.planning/codebase/ARCHITECTURE.md` (слоистый каскад vendor → тема → override) и `STRUCTURE.md`.
- **Известные concerns** (`.planning/codebase/CONCERNS.md`): header/footer дублируются на 11 страниц (нет шаблонизации → правка ×11); тяжёлый payload; `chart.js` 208 КБ не используется ни одной страницей; войны специфичности между темой и custom-слоем; картинки ~6.9 МБ без WebP; нет автотестов.
- **Шрифты:** Be Vietnam Pro + Plus Jakarta Sans с Google Fonts (внешняя зависимость).
- **QA:** автотестов нет. Проверка — вручную через Playwright + Chrome DevTools (responsive desktop/tablet/mobile, a11y цель 0 нарушений). Предыдущий аудит — `.planning` память `ui-audit-2026-06-23.md`.
- **Язык контента:** русский.

## Constraints

- **Tech stack**: правки только в `css/custom.css`, `css/base.css`, `js/custom.js` — vendor/theme read-only — чтобы не сломать обновляемость темы и не порождать регрессии
- **No-build**: нельзя вводить сборку/бандлер; всё работает открытием HTML в браузере
- **Logic-safe**: бизнес-логика, формы→WhatsApp, аналитика, роутинг, JSON-LD не должны измениться по поведению
- **Cross-device**: каждое изменение проверяется на desktop, tablet, mobile
- **A11y-floor**: Lighthouse/accessibility не должны стать хуже текущего baseline
- **Duplication**: header/footer на 11 страницах — общие правки придётся вносить согласованно во все файлы (нет include-механизма)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Audit-first: ничего не менять в коде до утверждённого плана + UI design contract | Требование заказчика; снижает риск регрессий в живой теме | — Pending |
| Все CSS-правки только в `custom.css`/`base.css`, JS — в `custom.js` | Vendor/theme read-only ради обновляемости; override-слой грузится последним | — Pending |
| Проверка изменений через Playwright (desktop/tablet/mobile) + a11y | Автотестов нет; это единственный надёжный способ верификации визуала | — Pending |
| Не вводить build-систему в этом milestone | Сохранить no-build простоту; оптимизация payload — кандидат в отдельный milestone | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-25 after initialization*
