(function () {
	'use strict';

	var WA_NUMBER = '77072370050'; // +7 707 237 00 50

	/* Иконки для инъекции (контакт в шапке + sticky-CTA). WA повторяет глиф
	   плавающей кнопки; PHONE — телефонная трубка (FontAwesome phone-solid).
	   aria-hidden: декоративны, доступное имя несёт aria-label/текст ссылки. */
	var WA_SVG = '<svg aria-hidden="true" viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>';
	var PHONE_SVG = '<svg aria-hidden="true" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>';

	document.addEventListener('DOMContentLoaded', function () {
		initMobileMenu();
		initWhatsAppFloat();
		initLeadForm();
		initMarqueeSpeed();
		initSvgAria();
		initSearchA11y();
		initHeaderContact();
		initStickyCta();
		initTrustCounters();
	});

	/* --- 1. Мобильное меню -----------------------------------------------
	   CSS темы открывает панель по классу .active на контейнере навигации
	   (.active .pbmit-menu-wrap / .active .pbmit-mobile-menu-bg). Кнопка
	   #menu-toggle уже есть в разметке, но обработчик отсутствует. */
	function initMobileMenu() {
		var toggle = document.getElementById('menu-toggle');
		var nav = document.getElementById('site-navigation');
		if (!toggle || !nav) return;

		var bg = nav.querySelector('.pbmit-mobile-menu-bg');

		function openMenu() {
			nav.classList.add('active');
			document.body.classList.add('pfg-menu-open');
		}
		function closeMenu() {
			nav.classList.remove('active');
			document.body.classList.remove('pfg-menu-open');
			/* Меню темы (js/gsap-animation.js:141-148) открывается классом .active на
			   <body> и на .pbmit-navbar > div, а НЕ на нашем #site-navigation. Снимаем
			   те же классы — иначе панель не уезжает. Особенно важно для крестика-клона
			   в sticky-шапке: тема вешает обработчик закрытия только на ОРИГИНАЛ
			   (gsap-animation.js:146), у клона .closepanel обработчика нет. remove
			   идемпотентен — итог всегда «закрыто». */
			document.body.classList.remove('active');
			/* .pbmit-navbar — и оригинал, и КЛОН в sticky-шапке (scripts.js клонирует
			   шапку вместе с классом .active на nav). Снимаем .active со всех navbar,
			   их div-детей и mega-wrap — иначе у клона остаётся активный предок и его
			   .pbmit-menu-wrap не уезжает. */
			document.querySelectorAll('.pbmit-navbar, .pbmit-navbar > div, .mega-menu-wrap').forEach(function (el) {
				el.classList.remove('active');
			});
		}

		toggle.addEventListener('click', function (e) {
			e.preventDefault();
			nav.classList.contains('active') ? closeMenu() : openMenu();
		});

		// Клик по затемнённому фону — закрыть
		if (bg) bg.addEventListener('click', closeMenu);

		/* Крестик «Закрыть» (.closepanel) тема инжектит в .pbmit-mobile-menu-bg
		   (gsap-animation.js:145) и навешивает обработчик ТОЛЬКО на оригинал; в клоне
		   sticky-шапки крестик остаётся без обработчика → меню не закрывалось. Делегируем
		   клик по любому .closepanel (и по затемнённому фону) на closeMenu. Фаза ВСПЛЫТИЯ
		   (не capture): срабатываем ПОСЛЕ возможного toggle темы, а closeMenu идемпотентен
		   (remove), поэтому итог всегда «закрыто» — без риска повторного открытия. */
		document.addEventListener('click', function (e) {
			var t = e.target;
			if (!t || !t.closest) return;
			if (t.closest('.closepanel') ||
				(t.classList && t.classList.contains('pbmit-mobile-menu-bg'))) {
				closeMenu();
			}
		});

		// Клик по обычной ссылке меню (без подменю) — закрыть
		nav.querySelectorAll('ul.navigation a').forEach(function (a) {
			a.addEventListener('click', function () {
				if (!a.parentElement.classList.contains('dropdown')) closeMenu();
			});
		});

		// Esc — закрыть
		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape') closeMenu();
		});
	}

	/* --- 2. Плавающая кнопка WhatsApp --------------------------------- */
	function initWhatsAppFloat() {
		if (document.querySelector('.pfg-whatsapp-float')) return;
		var a = document.createElement('a');
		a.className = 'pfg-whatsapp-float';
		a.href = 'https://wa.me/' + WA_NUMBER;
		a.target = '_blank';
		a.rel = 'noopener';
		a.setAttribute('aria-label', 'Написать в WhatsApp');
		a.innerHTML = '<svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>';
		document.body.appendChild(a);
	}

	/* --- 3. Форма заявки → WhatsApp ------------------------------------
	   Бэкенда нет (статический сайт). Форма с классом .pfg-form собирает поля
	   и открывает чат WhatsApp с готовым текстом обращения. */
	function initLeadForm() {
		var forms = document.querySelectorAll('.pfg-form');
		if (!forms.length) return;

		forms.forEach(function (form) {
			form.addEventListener('submit', function (e) {
				e.preventDefault();
				var status = form.querySelector('.pfg-form-status');

				var consent = form.querySelector('[name="consent"]');
				if (consent && !consent.checked) {
					if (status) {
						status.textContent = 'Пожалуйста, подтвердите согласие на обработку данных.';
						status.className = 'pfg-form-status is-error';
					}
					return;
				}

				var name = (form.querySelector('[name="name"]') || {}).value || '';
				var phone = (form.querySelector('[name="phone"]') || {}).value || '';
				var type = (form.querySelector('[name="biztype"]') || {}).value || '';
				var msg = (form.querySelector('[name="message"]') || {}).value || '';

				var text = 'Здравствуйте! Заявка с сайта taxpfg.kz.';
				if (name) text += '\nИмя: ' + name;
				if (phone) text += '\nТелефон: ' + phone;
				if (type) text += '\nФорма бизнеса: ' + type;
				if (msg) text += '\nВопрос: ' + msg;

				var url = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text);
				window.open(url, '_blank', 'noopener');

				if (status) {
					status.textContent = 'Открываем WhatsApp… Если чат не открылся, напишите нам на +7 707 237 00 50.';
					status.className = 'pfg-form-status is-ok';
				}
				form.reset();
			});
		});
	}

	/* --- 4. Замедление бегущей строки (marquee) ----------------------------
	   Тема инициализирует Swiper для .swiper-slider.marquee со speed:10000
	   (js/scripts.js — вендорный, НЕ редактируем). На таком значении строка
	   с названиями услуг бежит слишком быстро и не читается. Переопределяем
	   params.speed уже созданного экземпляра на бо́льшее значение: скорость
	   обратно пропорциональна speed, поэтому больше speed = медленнее ход.
	   Значение 40000 (~4× медленнее) подобрано и проверено визуально.

	   ВАЖНО: только присваиваем params.speed. Нельзя вызывать
	   autoplay.stop()/start() — в конфиге темы disableOnInteraction:true,
	   и пара stop→start трактуется как «взаимодействие», намертво
	   останавливая прокрутку. Автоплей читает this.params.speed на каждом
	   цикле run(), поэтому новое значение подхватывается само собой.

	   Тема может инициализировать Swiper как на DOMContentLoaded, так и
	   позже (window.load), поэтому опрашиваем экземпляр с интервалом и
	   переустанавливаем speed в течение ~10 c — это покрывает обе ситуации
	   и поправляет значение, если тема его переинициализирует. */
	function initMarqueeSpeed() {
		var MARQUEE_SPEED = 40000; // вендорное значение темы — 10000
		var el = document.querySelector('.swiper-slider.marquee');
		if (!el) return;

		var ticks = 0;
		var MAX_TICKS = 100; // ~10 c при шаге 100 мс
		var timer = setInterval(function () {
			ticks++;
			var sw = el.swiper;
			if (sw && sw.params && sw.params.speed !== MARQUEE_SPEED) {
				sw.params.speed = MARQUEE_SPEED;
			}
			if (ticks >= MAX_TICKS) clearInterval(timer);
		}, 100);
	}

	/* --- 5. aria-hidden для декоративных SVG соцсетей (WCAG 4.1.2) -----
	   SVG-иконки в .pbmit-social-links и .pbmit-footer-social-icon несут
	   только декоративную функцию. Добавляем aria-hidden, чтобы screen reader
	   не объявлял их как «graphic» или «image».
	   Идемпотентно: не переписываем уже установленный aria-hidden. */
	function initSvgAria() {
		document.querySelectorAll('.pbmit-social-links svg, .pbmit-footer-social-icon svg').forEach(function (svg) {
			if (!svg.getAttribute('aria-hidden')) {
				svg.setAttribute('aria-hidden', 'true');
			}
		});
	}

	/* --- 6. Доступное имя поля поиска (WCAG 1.3.1 «Info and Relationships», A)
	   Тема даёт input[type=search].search-field только с placeholder="Поиск …",
	   без <label>/aria-label → у поля нет программно доступного имени (placeholder
	   именем не считается). Поле скрыто до клика по иконке, но нарушение
	   фиксируется на всех страницах. HTML вендорный — проставляем имя из JS-слоя.
	   Идемпотентно: не перетираем уже заданный aria-label. */
	function initSearchA11y() {
		document.querySelectorAll('input.search-field, .pbmit-search-form input[type="search"]').forEach(function (inp) {
			if (!inp.getAttribute('aria-label')) {
				inp.setAttribute('aria-label', 'Поиск по сайту');
			}
		});
	}

	/* --- 7. Swiper H1-дубликат → aria-hidden (WCAG 2.4.1) ---
	   Swiper.js клонирует первый слайд в конец DOM для бесшовной анимации.
	   Слайд содержит <h1 class="pbmit-slider-title"> — возникает MULTI_H1.
	   После инициализации скрываем дубликат из accessibility tree.
	   Идемпотентно. */
	function initSwiperA11y() {
		var ticks = 0;
		var MAX_TICKS = 100; // ~10 c при 100-мс шаге
		var timer = setInterval(function () {
			ticks++;
			var sliders = document.querySelectorAll('.swiper-slider');
			sliders.forEach(function (swEl) {
				if (!swEl.swiper) return; // ещё не инициализирован
				// swiper-slide-duplicate создаётся после init
				var dup = swEl.querySelector('.swiper-slide-duplicate');
				if (dup) {
					var h = dup.querySelector('h1, h2');
					if (h && !h.getAttribute('aria-hidden')) {
						h.setAttribute('aria-hidden', 'true');
						h.setAttribute('tabindex', '-1');
					}
				}
			});
			if (ticks >= MAX_TICKS) clearInterval(timer);
		}, 100);
	}

	/* --- 8. Контакт в мобильной шапке (D1, конверсия) ---------------------
	   На ≤1200px тема прячет телефон и кнопку «Получить консультацию» — в шапке
	   остаются только логотип и гамбургер, и целевое действие (звонок/WhatsApp)
	   недоступно с первого экрана. 11 HTML — вендорно-дублированная разметка,
	   поэтому (как и .pfg-whatsapp-float) инжектим контакт из общего custom.js:
	   две иконки-ссылки 44×44 (tel: и WhatsApp) перед гамбургером. Видимость
	   задаёт CSS (.pfg-header-contact — только ≤1200px). Текст не вводим:
	   кнопки иконочные, доступное имя — aria-label. Идемпотентно. */
	function initHeaderContact() {
		/* Тема клонирует шапку в .pbmit-sticky-header → в DOM два .pbmit-right-area,
		   причём у клона id="menu-toggle" снят (остаётся только класс .nav-menu-toggle).
		   Поэтому берём ОСНОВНУЮ область (не внутри .pbmit-sticky-header), а гамбургер
		   ищем уже ВНУТРИ неё (гарантированный потомок → insertBefore не упадёт). */
		var area = Array.prototype.filter.call(
			document.querySelectorAll('.pbmit-right-area'),
			function (a) { return !a.closest('.pbmit-sticky-header'); }
		)[0];
		if (!area || area.querySelector('.pfg-header-contact')) return;

		var wrap = document.createElement('div');
		wrap.className = 'pfg-header-contact';
		wrap.innerHTML =
			'<a class="pfg-hc-btn pfg-hc-call" href="tel:+' + WA_NUMBER + '" aria-label="Позвонить: +7 707 237 00 50">' + PHONE_SVG + '</a>' +
			'<a class="pfg-hc-btn pfg-hc-wa" href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">' + WA_SVG + '</a>';

		var toggle = area.querySelector('.nav-menu-toggle, #menu-toggle');
		if (toggle) area.insertBefore(wrap, toggle);
		else area.appendChild(wrap);
	}

	/* --- 9. Sticky мобильная CTA-полоса (конверсия) ----------------------
	   Персистентный CTA для рекламного трафика на ТЕЛЕФОНАХ (≤576px): закреплённая
	   снизу полоса «позвонить | WhatsApp», видима с первого экрана. Именно на ≤576px
	   в шапке нет места для контакта рядом с длинным логотипом (DOM-замер: контакт
	   перекрывал бы логотип), поэтому полоса — основной мобильный контакт. На 577px+
	   контакт несут иконки шапки (раздел 8), и полоса скрыта (CSS). Полоса заменяет
	   плавающую кнопку на ≤1200 (CSS прячет .pfg-whatsapp-float), backtotop поднимается.

	   ОСОЗНАННО ВВОДИТ sticky-CTA, ранее зафиксированную как отсутствующую
	   (CNV-03, custom.css:42-50). Решение пересмотрено для конверсии под трафик
	   (docs/REDESIGN-BRIEF.md, Волна 1) — это supersede прежнего разрешения-по-отсутствию.
	   Текст не вводим: используем существующие строки (телефон, «WhatsApp»).
	   Поведение форм→WhatsApp не затрагивается. Идемпотентно. */
	function initStickyCta() {
		if (document.querySelector('.pfg-sticky-cta')) return;

		var bar = document.createElement('div');
		bar.className = 'pfg-sticky-cta';
		bar.innerHTML =
			'<a class="pfg-sticky-btn pfg-sticky-call" href="tel:+' + WA_NUMBER + '">' + PHONE_SVG + '<span>+7 707 237 00 50</span></a>' +
			'<a class="pfg-sticky-btn pfg-sticky-wa" href="https://wa.me/' + WA_NUMBER + '" target="_blank" rel="noopener">' + WA_SVG + '<span>WhatsApp</span></a>';
		document.body.appendChild(bar);
		/* Видимость полностью на CSS: полоса всегда видима на телефонах ≤576px
		   (в шапке там нет места для контакта рядом с длинным логотипом). Скролл-
		   гейт не нужен — для рекламного трафика контакт должен быть с первого
		   экрана. На 577px+ полоса скрыта (там контакт несут иконки шапки). */
	}

	/* --- 10. Анимация счётчиков доверия (D6, Волна 3) ---------------
	   IntersectionObserver + requestAnimationFrame, без зависимости от
	   jQuery/waypoints/numinate — те давали дёрганый счётчик на малых числах
	   (8, 11) и сбрасывали текст в «0» до появления в viewport.
	   easeOutQuart: быстрый разгон, плавное торможение на финальной цифре.
	   Класс .completed блокирует повторный запуск при скролле назад. */
	function initTrustCounters() {
		var counters = document.querySelectorAll('.pfg-trust-number[data-to]');
		if (!counters.length) return;

		function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); }

		function runCounter(el) {
			var to = parseInt(el.getAttribute('data-to')) || 0;
			var after = el.getAttribute('data-after') || '';
			var duration = 1400;
			var start = null;
			function step(ts) {
				if (!start) start = ts;
				var t = Math.min((ts - start) / duration, 1);
				el.textContent = Math.round(to * easeOutQuart(t)) + after;
				if (t < 1) requestAnimationFrame(step);
			}
			requestAnimationFrame(step);
			el.classList.add('completed');
		}

		var observer = new IntersectionObserver(function(entries) {
			entries.forEach(function(entry) {
				if (entry.isIntersecting && !entry.target.classList.contains('completed')) {
					runCounter(entry.target);
				}
			});
		}, { threshold: 0.4 });

		counters.forEach(function(el) { observer.observe(el); });
	}

	})();