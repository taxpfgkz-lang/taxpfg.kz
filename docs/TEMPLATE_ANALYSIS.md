# Анализ шаблона taxpfg.kz (для дальнейшей разработки сайта)

> Цель файла: зафиксировать, что представляет собой текущий шаблон, какие в нём
> есть готовые компоненты и что нужно заменить/доделать при сборке реального
> сайта PrimeFinance Group на его основе. Контент берём из `docs/SITE_CONTENT.md`.

## 1. Что это за шаблон
- Коммерческая HTML-тема **GudFin – Accounting and Finance Management** (студия
  PBMInfotech, классы `pbmit-*`). Тематика — бухгалтерия/финансы/консалтинг, то
  есть профильная под наш проект.
- Сейчас в проекте есть **только `index.html`** (Homepage 01). Меню ссылается на
  ~35 страниц (about-us, services, service-details, contact-us, faq, our-team,
  blog-*, portfolio-* и т.д.) — **их физически нет**, это демо-навигация темы.
- Язык документа `lang="en"`, контент — демо/English + «рыба» (lorem). Всё это
  заменяется русским контентом.
- `<meta name="robots" content="noindex, follow">` — для прода поменять на
  индексируемый.

## 2. Технологический стек (подключено в index.html)
**CSS (12 файлов в `css/`):** bootstrap.min, fontawesome, pbmit_gudfin (иконочный
шрифт темы), pbminfotech-base-icons, themify-icons, swiper.min, magnific-popup,
aos, shortcode (основные стили шорткодов темы), base, style, responsive.

**JS (в `js/`):** jquery.min, popper, bootstrap.min, waypoints, appear, numinate
(счётчики), swiper.min (слайдеры), magnific-popup (лайтбокс видео/галерея),
circle-progress, countdown, aos (анимации появления), gsap + ScrollTrigger +
SplitText + gsap-animation (tween-эффекты), theia-sticky-sidebar, chart.js
(графики), scripts.js (инициализация всего).

**Инициализация (js/scripts.js):** Swiper создаётся по data-атрибутам;
`AOS.init()`; счётчики через `[data-appear-animation="animateDigits"]` + numinate;
видео-лайтбокс через magnificPopup; back-to-top; график —
`createBarChart('myChart', ['Budget','Saving','Analytic'], [135,120,100], [95,90,65])`.
→ Новые страницы достаточно собрать на той же разметке и подключить тот же набор
скриптов — поведение заведётся само.

**Иконочные шрифты (`fonts/`):** fontawesome, themify, pbmit_gudfin,
pbminfotech-base-icons. Иконки используются и инлайн-SVG, и через классы
`pbmit-base-icon-*`.

## 3. Карта секций главной (index.html, 1801 строка)
| Строки | Секция | Компонент / что переиспользуем |
|---|---|---|
| 42–335 | Header | Sticky-хедер, лого (logo-white.svg / logo-dark.svg), «Book a call» + WhatsApp, мегаменю, поиск, кнопка «Get in touch», телефон, мобильный toggle |
| 220–333 | Hero | Swiper fade-слайдер, 3 слайда: фон `slider1-0X.jpg` + `<video>` на каждом слайде |
| 340–399 | Info boxes | `pbmit-ihbox-style-4` — 4 преимущества с SVG-иконками |
| 401–477 | About | 2 фото (about-01.jpg, about-02.png) + счётчик `numinate` (25+) + текст + кнопка |
| 479–660 | Services | `pbmit-element-service-style-2` — сетка из 5 карточек услуг + 1 карточка-CTA |
| 662–713 | Marquee | Бегущая строка ключевых слов |
| 715–820 | Why Choose Us | График Chart.js (`#myChart`) + список + 3 «static box» с фоновыми фото |
| 822–846 | Video | Кнопка-лайтбокс YouTube (magnific) + tween-заголовок |
| 848–938 | Process | 4 шага, Swiper-слайдер с картинками `processbox-img-0X.png` |
| 940–1073 | Team | Слайдер команды (team-0X.jpg) |
| 1075–1258 | Testimonials | Слайдер отзывов |
| 1260–1418 | Client Satisfaction | Счётчики/статистика |
| 1420–1545 | Blog | 3 карточки (blog-0X.jpg) |
| 1550–1726 | Footer | CTA «Let's Discuss» с вращающимся «Contact», виджеты-меню, форма подписки, Email/Location/Call, копирайт, соцсети |
| 1731–1759 | Прочее | Оверлей поиска + кнопка «наверх» |

> Inner-страницы (about/services/contact) в теме обычно имеют **titlebar/breadcrumb**
> (баннер заголовка), в `index.html` его нет, но в ассетах есть `titlebar-img.jpg`
> — разметку titlebar для внутренних страниц нужно будет собрать.

## 4. Плейсхолдеры, которые надо заменить ВЕЗДЕ
- `lang="en"` → `lang="ru"`; `<title>` и `<meta description>`; `robots` noindex → индексируемый.
- Лого/бренд «Gudfin» (текст и SVG) → PrimeFinance Group.
- Телефоны: `1 440 848 8222`, `(000)123456789`, `+1 440 848 8222` → **+7 707 237 00 50**.
- Email: `[email protected]` (обфусцирован Cloudflare) → реальный e-mail (уточнить) через обычный `mailto:`.
- Адрес: `174 Street Charleston, New York` → **Алматы, пр. Абая 68/74, БЦ «AVENUE CITY», офис 39**.
- Копирайт: `© 2025 Gudfin` → © PrimeFinance Group, актуальный год.
- WhatsApp-ссылка в «Book a call» → `https://wa.me/77072370050`.
- Соцсети (#) и пункты меню футера → реальные (уточнить, какие соцсети есть).
- Весь демо/английский текст и «рыба» (lorem) → русский контент из `SITE_CONTENT.md`.

## 5. Технический «мусор» от исходного хостинга (убрать на нашем деплое)
- Cloudflare beacon (`static.cloudflareinsights.com/...`) и инлайн `__CF$cv$params`.
- Email-обфускация Cloudflare: `js/email-decode.min.js` + ссылки `/cdn-cgi/l/email-protection#...` → заменить на прямой `mailto:`.

## 6. Отсутствующие ассеты / что готовить
- **`images/slider-video.mp4` отсутствует** — hero-`<video>` на всех 3 слайдах
  ссылается на несуществующий файл (нужно подобрать видео или убрать видео-слой).
- Демо-изображения присутствуют, но нерелевантны (team-0X, blog-0X, slider1-0X,
  about-0X, static-box-0X, processbox-img-0X) → подбирать/скачивать новые
  тематические изображения и заменять.
- `fevicon.png` — заменить на фавикон PFG.

## 7. Маппинг наших страниц на типы шаблона (план сборки)
| Наша страница (SITE_CONTENT.md) | На базе какого типа темы |
|---|---|
| Главная | `index.html` (Homepage 01) — адаптировать секции под наш контент |
| О компании | страница типа `about-us` + titlebar |
| Услуги (обзор) | `services` (сетка карточек service-style-2) + titlebar |
| Бухгалтерское сопровождение | `service-details` + titlebar |
| Налоговый учёт и отчётность | `service-details` + titlebar |
| Регистрация и сопровождение бизнеса | `service-details` + titlebar |
| Восстановление и постановка учёта | `service-details` + titlebar |
| Консультации и налоговый юрист | `service-details` + titlebar |
| Контакты | `contact-us` (форма + карта + контакты) + titlebar |

> Лишние демо-разделы темы (portfolio, blog-сетки, our-history, team-member-detail,
> homepage-2..5) на реальном сайте не нужны — из меню убираем, оставляем только
> наши страницы.

## 8. Вывод
Шаблон профильный и технически самодостаточный (все стили/скрипты локальные,
без сборки/npm — статичный HTML). Подходит как основа: переиспользуем хедер,
футер, hero-слайдер, карточки услуг, info-box, счётчики, процесс, отзывы и т.д.
Работа сведётся к: (1) очистке от демо-контента и внешнего «мусора»,
(2) русификации и подстановке контента из `SITE_CONTENT.md`, (3) сборке
недостающих внутренних страниц по типам темы, (4) подбору и замене изображений,
(5) настройке форм, контактов и SEO-мета.
