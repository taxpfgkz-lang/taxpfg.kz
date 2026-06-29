## Session — 2026-06-27 00:00

### Goal
Execute all remaining milestone phases autonomously using the discuss → plan → execute flow, then run milestone lifecycle if all phases complete.

### Starting state
`AGENT_SESSION_LOG.md` did not exist. `.planning/STATE.md` shows milestone `v1.0` in executing status with current focus on Phase 4. `.planning/ROADMAP.md` shows Phases 4 and 5 incomplete. `gsd-tools query init.milestone-op` and `roadmap.analyze` confirm Phase 4 is partial and Phase 5 has not started.

### Action plan
1. Execute remaining Phase 4 workflow steps and resolve verification routing.
2. Execute full Phase 5 workflow and resolve verification routing.
3. If all phases complete, run milestone audit, completion, and cleanup.
4. Update planning state and session log after each significant step.

### Critical context
- Runtime is `claude`, so autonomous plan/execute run inline rather than backgrounded.
- `.planning/config.json` has `workflow.skip_discuss=false`, `workflow.ui_phase=true`, `workflow.code_review=true`; `workflow.ui_review` is absent, so autonomous workflow falls back to its documented default `true`.
- User only wants pauses for explicit decisions, blockers, or validation requests.

### Step — 2026-06-27 00:05

#### Action
Inspected milestone state with `.planning/STATE.md`, `.planning/ROADMAP.md`, and `gsd-tools` milestone/roadmap queries to identify remaining work.

#### Files
- `.planning/STATE.md` — read current milestone progress and current phase marker.
- `.planning/ROADMAP.md` — read incomplete phases and pending plans.
- `AGENT_SESSION_LOG.md` — created session log and recorded the restored context.

#### Result
Confirmed that Phase 4 is partially executed with pending `04-03` and `04-04` work, and Phase 5 has not started. Confirmed runtime is `claude`, so discuss/plan/execute must run inline.

#### Verification
- `node "C:/Users/Администратор/.config/opencode/gsd-core/bin/gsd-tools.cjs" query init.milestone-op` — success.
- `node "C:/Users/Администратор/.config/opencode/gsd-core/bin/gsd-tools.cjs" query roadmap.analyze` — success.
- `node "C:/Users/Администратор/.config/opencode/gsd-core/bin/gsd-tools.cjs" query init.phase-op 4` — success.

#### Next step
Run the autonomous execution flow for Phase 4, then inspect verification routing and any required user decision.

### Step — 2026-06-27 00:12

#### Action
Attempted to advance Phase 4 execution through the existing GSD workflow path and then inspected the resulting worktree and phase artifacts.

#### Files
- `.planning/phases/04-conversion-blocks-imagery/` — checked for new summaries, verification, and review artifacts.
- `css/custom.css` — worktree shows Phase 4 CSS additions for footer density, image object-fit, and tablet title-bar tier.
- `404.html`, `about.html`, `accounting-recovery.html`, `accounting.html`, `consulting.html`, `index.html`, `privacy.html`, `registration.html`, `taxes.html` — worktree now contains broad content/navigation/meta changes.
- `.planning/STATE.md` — re-checked and confirmed it was not advanced by the attempted execution.

#### Result
The attempted execution left real site changes in the worktree but did not produce the expected GSD artifacts (`04-03-SUMMARY.md`, `04-04-SUMMARY.md`, `04-VERIFICATION.md`, `04-REVIEW.md`) and did not update `.planning/STATE.md`. The current diff also includes scope-expanding content/SEO edits that are not obviously limited to Phase 4 footer/img goals.

#### Verification
- `git status --short` — confirmed modified site pages and missing new phase artifacts.
- `git diff -- ...` on the touched pages and `css/custom.css` — confirmed CSS changes plus unrelated copy/meta/navigation edits.
- `grep` in `.planning/phases/04-conversion-blocks-imagery/*.md` — found no new verification/review status outputs.

#### Next step
Pause for a user decision because the workflow produced out-of-scope edits without verification artifacts; determine whether to keep and reconcile them, discard them, or stop autonomous mode.

### Decision — 2026-06-27 00:18

#### Context
Phase 4 retry surfaced broad HTML/content edits that exceeded the `04-03` plan scope, while the CSS work for footer density, imagery sizing, and tablet title-bar looked aligned with the plan.

#### Options considered
1. Keep all generated edits and continue — fastest, but violates the phase boundary and leaves unverified copy/SEO changes in the milestone.
2. Revert only the out-of-scope HTML edits and keep the in-scope CSS work — preserves the legitimate Phase 4 changes while restoring plan discipline.
3. Revert everything and restart Phase 4 from scratch — safest, but discards apparently correct CSS progress without evidence of a problem there.

#### Decision
Chose option 2 after user confirmation (`Fix and retry`). Reverted the out-of-scope HTML edits and retained the CSS-only changes that match `04-03-PLAN.md`.

#### Trade-offs
This keeps the worktree focused on the planned footer/img/title-bar changes, but Phase 4 still needs explicit verification artifacts and final human validation before it can be marked complete.

#### Reversible?
Yes. The retained CSS change is still local and can be reverted if verification fails.

### Step — 2026-06-27 00:20

#### Action
Reverted Phase 4 out-of-scope HTML edits and re-validated the remaining `04-03` CSS-only implementation against the plan's static gates.

#### Files
- `404.html`, `about.html`, `accounting-recovery.html`, `accounting.html`, `consulting.html`, `index.html`, `privacy.html`, `registration.html`, `taxes.html` — reverted out-of-scope markup/content/meta edits.
- `css/custom.css` — retained the in-scope Phase 4 plan-03 CSS block for footer density, image object-fit, and tablet title-bar tier.

#### Result
The worktree now keeps only the `css/custom.css` changes relevant to `04-03-PLAN.md`. Static checks confirm the CSS contains the expected `object-fit` and tablet-tier rules, and the filtered functional `!important` count is `60`, matching the plan's allowed single T1 exception.

#### Verification
- `git checkout -- ...html` — success.
- `python -c "... !important count ..."` — returned `60`.
- `python -c "... object-fit + media query presence ..."` — returned `True True`.

#### Next step
Create the `04-03` execution summary and run the `04-04` verification gate (DOM/axe/Lighthouse/VER-04 + human validation routing).


### Step — 2026-06-27 00:40

#### Action
Executed Phase 4 plan 03 implementation by appending the planned CSS-only footer density, imagery object-fit, and tablet title-bar tier overrides.

#### Files
- `css/custom.css` — added Phase 4 "ЭТАП 16" block for CNV-04 mobile footer density, IMG-01 wrapper-scoped `object-fit`, and T1 tablet title-bar min-height override.

#### Result
Plan 03 implementation now exists in the working tree. Footer parity remains CSS-only, imagery sizing is scoped to theme photo wrappers, and the 768→576 title-bar tier is defined with one vendor-cited `!important` on `min-height`.

#### Verification
- `css/custom.css` inspected after edit; new rules appended after the existing Phase 4 pricing block.
- Full DOM/a11y verification still pending in Phase 4 plan 04.

#### Next step
Create the `baseline/measure-phase4.cjs` phase-gate script, run the available automated checks, and classify any missing gates explicitly.

## Session — 2026-06-27 00:45

### Goal
Restore the interrupted autonomous milestone run, finish Phase 4 verification routing, then continue remaining phases and lifecycle.

### Starting state
Read the prior session log, .claude/CLAUDE.md, .planning/STATE.md, and .planning/ROADMAP.md. Actual files confirm Phase 4 still has 04-03 and 04-04 incomplete, while css/custom.css already contains the Phase 4 Stage 16 CSS block. No README.md exists.

### Action plan
1. Verify the current Phase 4 implementation against 04-03/04-04 plan requirements.
2. Create the missing Phase 4 summaries/artifacts and run the verification gate.
3. Route Phase 4 verification outcome, then continue autonomous execution into Phase 5.
4. If all phases complete, run milestone audit, completion, and cleanup.

### Critical context
- Runtime remains non-Codex, so autonomous plan/execute run inline.
- Project rules still prefer css/custom.css and js/custom.js edits; vendor/theme files remain read-only.
- Existing Phase 4 CSS lives at css/custom.css:1338-1412 and must be verified rather than reimplemented blindly.

---

## Session — 2026-06-29 12:00 (ручная правка hero + фикс мобильного меню)

### Цель
Доработка hero-блока и исправление бага мобильного меню по запросу пользователя.

### Контекст
- Проект: taxpfg.kz (статический сайт на темплейте HTML/CSS/JS)
- Ветка: master (последний коммит 0bc3880 "feat(wave3): секция доверия D6")
- Рабочий режим: ручные правки по запросу пользователя, без GSD-воркфлоу
- Локальный HTTP-сервер: порт 8731 (http://localhost:8731/)
- Тестирование: Playwright (mobile 375/390, desktop 1440)

### Выполнено

#### 1. Центрирование hero-блока на index.html (mobile + desktop)

**Запрос:** hero = 100vh; заголовок одной строкой по центру, кнопка под ним по центру, описание двумя строками по центру под кнопкой.

**Изменения в `css/custom.css` (§20, строки ~1905+):**
- Hero = 100svh (вместо вендорных фикс. высот 1000/880/700px), min-height 600px
- Flexbox-центрирование `.pbmit-slider-content` и `.video-content-area`
- Заголовок: fluid font-size `clamp(30px, 7.4vw, 122px)`, `white-space: nowrap` только на ≥768px (на мобильном <768px переносится в 2 строки естественно, чтобы не обрезаться)
- Оффер: 22px/500, центрирован, плашка с золотым акцентом снизу, `!important` для победы над Bootstrap `.d-flex .justify-content-end`
- Мобильный оффер (§20.4): снят вендорный `display:none` на ≤767px; оффер показан под кнопкой, 15px, переносы естественные

**Изменения в `index.html`:**
- Убраны `<br>` из заголовков трёх слайдов hero (`.pbmit-slider-one`)
- Исправлен невалидный тег `</h1>` → `</h2>` в слайде 1 (строка 171)
- Добавлен cache-busting `?v=20260629` к подключению `css/custom.css` (строка 54)

**Проверка:**
- Desktop 1440×900: hero=900px (100svh), заголовок одной строкой 106px по центру (cx=713), кнопка/оффер по центру, нет h-scroll
- Mobile 390×844: заголовок в 2 строки (без обрезки), кнопка + оффер по центру (cx≈188), нет h-scroll, не перекрывает sticky-полосу

#### 2. Фикс крестика «Закрыть» в мобильном меню

**Баг:** крестик `.closepanel` в мобильном меню не закрывал панель при клике.

**Корень:** тема `js/gsap-animation.js:141-148` открывает меню классом `.active` на `<body>` и `.pbmit-navbar`, инжектит крестик в `.pbmit-mobile-menu-bg` оригинала и навешивает обработчик ТОЛЬКО на оригинал. Шапка клонируется в sticky-версию (`js/scripts.js`), у крестика-клона обработчика нет. `custom.js` закрывал только свой `#site-navigation`, но не снимал `.active` с `body` и `.pbmit-navbar` → панель оставалась открытой.

**Фикс в `js/custom.js` (строки 28-63, функция `initMobileMenu`):**
- `closeMenu()` теперь снимает `.active` со **всех** `.pbmit-navbar`, их `> div`, `body`, `.mega-menu-wrap` — те же переключатели, что у темы (идемпотентно)
- Делегирование клика по любому `.closepanel` (и по фону `.pbmit-mobile-menu-bg`) на `closeMenu` через всплытие (не capture) — крестик-клон и оригинал работают

**Изменения cache-busting:**
- `index.html`: добавлен `?v=20260629` к `js/custom.js` (строка 1118)
- Все 10 остальных страниц (`about.html`, `services.html`, `accounting.html`, `accounting-recovery.html`, `taxes.html`, `consulting.html`, `registration.html`, `contacts.html`, `privacy.html`, `404.html`): добавлен `?v=20260629` к `custom.css` и `custom.js` (строки 55 и ~580 в каждой)

**Проверка:**
- Реальные клики (page.mouse) на index.html и about.html (mobile 390/375): открытие гамбургером, закрытие крестиком, закрытие фоном, повторный цикл — всё работает
- Обе панели (оригинал + клон) закрываются (x=875, right=-400px, opacity=0, body.active=false)

### Файлы изменены
- `css/custom.css` — новая секция §20 (~1905+): hero 100svh, центрирование, мобильный оффер
- `js/custom.js` — функция `initMobileMenu` (строки 28-63): фикс закрытия меню крестиком
- `index.html` — cache-busting `?v=20260629`, убраны `<br>` в hero-заголовках, фикс `</h1>`→`</h2>`
- Все 11 HTML-страниц — cache-busting `?v=20260629` для `custom.css` и `custom.js`

### Проверки выполнены
- `python -m http.server 8731` — сервер работает
- Playwright: тестирование на mobile 375/390 и desktop 1440×900
  - Hero центрирован, заголовок/кнопка/оффер по центру (desktop: одна строка, mobile: 2 строки)
  - Крестик меню закрывает панель на index.html и about.html (реальные клики)
  - Нет горизонтального скролла, нет наложения на sticky-полосу

### Открытые задачи
- **Доработка кнопки меню (гамбургер):** пользователь запросил сделать её "красивее, аккуратнее" (скриншот приложен). Разметка прочитана (`index.html:152-154` — SVG с 4 точками), стили в `css/responsive.css:796-825, 2151-2159` (40×40 на tablet+, 45×45 на mobile, белый фон). Следующий шаг — определить концепцию редизайна и применить CSS-правки.

### Следующие шаги
1. Уточнить у пользователя желаемый вид кнопки меню (минималистичный стиль, другая иконка, убрать белую плашку и т.д.)
2. Применить CSS-правки в `css/custom.css` (переопределение `.nav-menu-toggle` для аккуратного вида)
3. Проверить на мобильном/планшетном вьюпорте (375/390/768)
4. Продолжить обход сайта по запросу пользователя ("буду пробегаться по сайту")

### Команды проекта
- **Dev-сервер:** `python -m http.server 8731` или `! python -m http.server 8731` (фон)
- **Тестирование:** через Playwright (запускается автоматически в беседе)
- **Git:** `git status`, `git diff`, `git add`, `git commit`
- **Деплой:** не настроен (статический сайт, загрузка на хостинг вручную)

### Ручные действия
Нет — все изменения протестированы и готовы к использованию. Пользователь продолжает обход сайта.

---

## Session — 2026-06-29 13:00 (аккуратная кнопка меню в ряд контакт-кнопок)

### Цель
Кнопка меню (`.nav-menu-toggle`) выпадала из ряда шапки: вендорная белая плашка
55×55 (45×45 @≤767) radius:5px с иконкой-сеткой 40×40 тёмного цвета — рядом с
золотой кнопкой-телефоном и зелёной WhatsApp (`.pfg-hc-btn`). Запрос Юрия: сделать
кнопку красивее и «одинаково с кнопочками».

### Диагностика (важно для будущих сессий)
- Скриншот Юрия = реальное состояние диска/прод. Браузер сперва показывал золотую
  44×44 версию — это был **устаревший кэш** `custom.css?v=20260629` (cache-buster
  зафиксирован, браузер держал старую версию с экспериментальным правилом, убранным
  с диска). Подтверждено: в custom.css селектора `.nav-menu-toggle` не было (только
  комментарий :161). Форс-перезагрузка стилей с диска вернула истинную вендорную
  белую кнопку. Вывод: при cache-buster `?v=` всегда форсить свежую загрузку перед
  DOM-замером (link.href с новым query), иначе DOM врёт из кэша.

### Выполнено
- **`css/custom.css`** — новый блок §17.1b (после `.pfg-hc-btn`, перед §17.2),
  `@media (max-width:1200px)`: `.nav-menu-toggle` → 44×44, `border-radius:var(--pfg-radius-sm)`,
  фон `rgba(236,171,35,.16)` (= `.pfg-hc-call`), flex-центрирование, transition;
  иконка svg/g → 20×20, `fill:var(--pfg-gold-deep) !important` (`!important` нужен,
  чтобы перебить sticky-клон `responsive.css:822-824`, спец. 0,3,1); `:active` →
  `translate(0,-50%) scale(.94)` (сохранён вендорный translateY для position:absolute).
  Позиционирование темы (right:0) НЕ тронуто. Гейт ≤1200 совпадает с `.pfg-header-contact`.
- **Бамп cache-buster:** `custom.css?v=20260629` → `?v=20260629b` на всех 11 HTML
  (чтобы правка доехала до вернувшихся посетителей; JS не менялся — его буфер не трогал).

### Проверки (Playwright, свежая загрузка с диска)
- 1060px и 768px: три кнопки идентичны — 44×44, center-y=42 (в одну линию), radius
  10px, иконки 20×20; меню = золотой-тинт + gold-deep иконка (точь-в-точь телефон).
- 390px (≤576): кнопка меню 44×44 золотая; контакт-иконки скрыты (их роль у sticky-полосы);
  горизонтального скролла нет.
- Функция меню: открытие кнопкой → `body.active/pfg-menu-open/navbar.active = true`;
  закрытие видимым крестиком → всё `false`. JS-поведение не сломано.
- Sticky-клон `#menu-toggle2`: 44px/radius10/золотой-тинт, иконка 20×20, fill gold-deep
  на svg/g/path — `!important` перебил вендорный fill клона (спец. 0,3,1).

### Файлы изменены
- `css/custom.css` — блок §17.1b (~37 строк)
- 11 HTML — cache-buster `custom.css?v=20260629b`

### Производственная готовность
production-ready: yes (CSS-only, обратимо, vendor read-only соблюдён, кросс-девайс +
функция + sticky-клон проверены DOM-замером). Не закоммичено (по правилу — коммит
только по запросу).

### Ручные действия
Нет.

---

## Session — 2026-06-29 13:45 (кнопка шапки «Получить консультацию» → WhatsApp)

### Цель
Запрос Юрия: header-CTA «Получить консультацию» должна открывать WhatsApp (была ссылка
на contacts.html).

### Контекст / точность scope
«Получить консультацию» встречается в 3 контекстах: (1) ШАПКА `.pbmit-header-button >
a.pbmit-btn` (стр. 125-127, глубокий отступ, на всех 11), (2) контентный/футерный CTA
`.pbmit-header-button` (стр. 320+, на 5 стр.), (3) оверлеи карточек `a.pbmit-link`
(пустые, стр. 232+). Юрий просил ИМЕННО шапку → меняем только (1).

### Выполнено
- **11 HTML** — в шапке `<a href="contacts.html" class="pbmit-btn">` →
  `<a href="https://wa.me/77072370050" target="_blank" rel="noopener"
  aria-label="Получить консультацию в WhatsApp" class="pbmit-btn">`.
  Точечно через `sed -i '120,140 s#...#...#'` (диапазон строк бракетит только шапку;
  контентные CTA на 320+ и оверлеи не задеты). Плоский wa.me без pre-fill — как у
  прочих прямых WA-точек (.pfg-hc-wa, sticky-полоса, float); pre-fill только у формы.
- HTML-документы не версионируются `?v=` → cache-buster не нужен.

### Проверки
- grep: 0 шапочных кнопок осталось на contacts.html; 9 контентных CTA + 11 оверлеев →
  contacts.html НЕ тронуты; 11 шапочных → wa.me.
- JS: клик по кнопке не перехватывается (custom.js делегирует только .closepanel/фон
  и `ul.navigation a`; кнопка — обычная ссылка).
- Playwright (1440, index): href=wa.me, target=_blank, rel=noopener, aria-label ✓ на
  оригинале И sticky-клоне. Реальный клик: defaultPrevented=false, открылся popup
  `api.whatsapp.com/send/?phone=77072370050` (чат с +7 707 237 00 50, без pre-fill).

### Файлы изменены
- 11 HTML — только строка header-CTA (шапка).

### Производственная готовность
production-ready: yes (обратимо, vendor read-only соблюдён, поведение проверено реальным
кликом). Не закоммичено (коммит только по запросу).
Возможное улучшение (по желанию): pre-fill текст «Здравствуйте! Хочу получить
консультацию.» в `?text=` для роста конверсии — пока плоская ссылка для единообразия.

### Ручные действия
Нет.

---

## Session — 2026-06-29 15:00 (убрать поиск + починить sticky-шапку)

### Цель
Запрос Юрия: (1) убрать поиск из шапки; (2) sticky-шапка (фикс при скролле) должна
выглядеть как обычная — сейчас «абсолютно разные»; (3) у sticky сломаны цвета —
«серо-белое непонятное», починить.

### Диагностика
- Поиск: кнопка `.pbmit-header-search-btn` (шапка) + скрытый оверлей-форма
  `.pbmit-header-search-form` (Search Box, ~стр.1034-1051). По 1× на стр.
- Sticky «серо-белое»: вендор (shortcode.css:3985-4024) делает sticky БЕЛОЙ
  (`rgba(white,.9)`, тёмный логотип, тёмная навигация, скрыты CTA+телефон). Наш
  стеклянный `backdrop-filter:blur` (§9.3, custom.css:446-452) ложится на ПРОЗРАЧНЫЙ
  header-content поверх бело-полупрозрачной обёртки → мутно-серое frosted-пятно. Плюс
  золотой активный пункт на белом ~1.9:1 нечитаем. Обычная шапка — тёмное стекло на
  фото-герое, белый логотип, бело-золотая навигация, золотая кнопка.

### Выполнено
- **11 HTML** — удалены `.pbmit-header-search-btn` и блок `.pbmit-header-search-form`
  (Python-regex, dry-run: по 1 совпадению/файл; `initSearchA11y` безопасен при отсутствии —
  forEach по пустому NodeList).
- **css/custom.css §9.3b** — sticky приведена к виду обычной (тёмной). `@media ≥1201`,
  специфичность 0,5,0 (`.site-header.pbmit-header-style-1 .pbmit-sticky-header.pbmit-fixed-header`)
  бьёт вендор 0,4,0 без !important:
  - фон обёртки `rgba(22,34,45,.92)` (ink) вместо white-.9 + тень-отрыв;
  - белый (main) логотип виден, тёмный (sticky) скрыт;
  - неактивная навигация белая (вендор делал blackish), активная — золото;
  - CTA-кнопка показана (вендор прятал); телефонный блок скрыт (как в обычной шапке);
  - у header-content убран дубль box-shadow от §9.3 (тень несёт обёртка).
- **Бамп cache-buster** custom.css `?v=20260629b → 20260629c` на 11 стр.

### Проверки (Playwright, desktop 1440 + mobile 390)
- Обычная шапка (скрин): поиск убран; логотип + навигация + золотая кнопка — чисто.
- Sticky (computed + elementsFromPoint, scrollY 1278): `active`, фон `rgba(22,34,45,.92)`,
  логотип белый (main inline-block / sticky none), навигация неактив=white активе=gold,
  CTA `display:block`, телефон `none`, поиска нет. `elementsFromPoint(720,45)` →
  sticky-`UL.navigation` сверху (рисуется, z=9, предки без transform/filter).
  ВАЖНО: Playwright НЕ скриншотит `position:fixed` sticky этой темы при программном
  скролле (артефакт компоновки fixed-слоёв) — обычная шапка (нормальный поток)
  скриншотится штатно. Истинность подтверждена computed-замером + тем, что пользователь
  sticky видит. → Юрию: hard-refresh и глянуть sticky вживую.
- Mobile 390: поиск (кнопка+форма) отсутствует, логотип+меню на месте, меню
  открывается/закрывается, h-scroll нет. Sticky-CSS гейтнут ≥1201 — мобайл не затронут.

### Файлы изменены
- 11 HTML — удалён поиск (кнопка+форма) + cache-buster `?v=20260629c`.
- css/custom.css — §9.3b (sticky-шапка).

### Производственная готовность
production-ready: yes (vendor read-only соблюдён, обычная+mobile проверены полностью,
sticky — computed-замером; визуальная верификация sticky за Юрием из-за лимита Playwright).
Не закоммичено (коммит только по запросу).

### Ручные действия
Юрию: открыть сайт с hard-refresh (Ctrl+F5), проскроллить вниз и вверх — убедиться,
что фиксированная шапка тёмная и совпадает с обычной.

---

## Session — 2026-06-29 14:15 (удалить блок «Напишите в WhatsApp» из шапки)

### Цель
Запрос Юрия: убрать из шапки блок «Напишите в WhatsApp + номер» — он избыточен, т.к.
кнопка «Получить консультацию» теперь ведёт в WhatsApp.

### Контекст / точность scope
Удаляемый блок — `.ihbox-style-17-wrap` (`.pbmit-ihbox-style-17`, левая группа рядом с
логотипом, index.html:75-91): «Напишите в WhatsApp» + WhatsApp-svg + `<a href=wa.me>номер`.
СОХРАНЕНЫ: телефонный блок `.pbmit-ihbox-style-3` («Нужна консультация?» + tel:,
строки 136-150) — другой канал; кнопка-CTA «Получить консультацию» → wa.me.
Прим.: на contacts.html «Напишите в WhatsApp» встречается 2× (второй — в контенте
страницы); якорь `ihbox-style-17-wrap` (1× на всех) гарантировал удаление только шапки.

### Выполнено
- **11 HTML** — удалён блок `.ihbox-style-17-wrap` (по 1718 симв, идентичен на всех).
  Метод: Python-regex `[ \t]*<div class="ihbox-style-17-wrap">.*?</a></h2>\s*</div>×4\n?`
  (DOTALL, non-greedy до ПЕРВОГО `</a></h2>` → берёт WhatsApp-h2, не телефонный).
  Dry-run перед применением: на всех 11 ровно 1 совпадение, в блоке есть «Напишите в
  WhatsApp», НЕТ `tel:+` и НЕТ «Получить консультацию» (safe=True).
- В custom.css ссылок на `ihbox-style-17` нет → чистка CSS не требуется.

### Проверки
- grep: `ihbox-style-17-wrap` = 0 везде; «Нужна консультация?» = 11; header-CTA
  `aria-label="Получить консультацию в WhatsApp"` = 11.
- Playwright desktop (1600/1440): блок отсутствует (`hasWaBlock=false`), левая группа
  шапки = только `site-branding` (логотип, без пустого враппера), nav/search/CTA(wa.me)
  целы, h-scroll нет. Скрин: логотип слева + меню + золотая кнопка справа.
- Playwright mobile (390): блок отсутствует, логотип + кнопка-меню видимы, h-scroll нет.
- Телефонный блок `.pbmit-ihbox-style-3` не тронут (на главной шапке его display:none —
  поведение темы, был таким и до правки; виден в sticky-шапке).

### Файлы изменены
- 11 HTML — удалён header-блок `.ihbox-style-17-wrap`.

### Производственная готовность
production-ready: yes (обратимо, vendor read-only соблюдён, кросс-девайс проверен,
телефон/CTA сохранены). Не закоммичено (коммит только по запросу).

### Ручные действия
Нет.
