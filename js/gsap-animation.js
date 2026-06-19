(function ($) {
	"use strict";

	gsap.registerPlugin(ScrollTrigger, SplitText);
	gsap.config({
		nullTargetWarn: false,
		trialWarn: false
	});
	/*----  Functions  ----*/
	function getpercentage(x, y, elm) { 
		elm.find('.pbmit-fid-inner').html(y + '/' + x);
		var cal = Math.round((y * 100) / x);
		return cal;
	}

	/*----  Title Animation  ----*/
	function pbmit_title_animation() {
		ScrollTrigger.matchMedia({
			"(min-width: 1025px)": function() {
				var pbmit_var = jQuery('.pbmit-custom-heading, .pbmit-heading-subheading');
				if (!pbmit_var.length) {
					return;
				}
				const quotes = document.querySelectorAll(".pbmit-custom-heading .pbmit-title , .pbmit-heading-subheading .pbmit-title");
				quotes.forEach(quote => {
					var getclass = quote.closest('.pbmit-custom-heading ,.pbmit-heading-subheading').className;
					var animation = getclass.split('animation-');
					if (animation[1] == "style1") return
					//Reset if needed
					if (quote.animation) {
						quote.animation.progress(1).kill();
						quote.split.revert();
					}
					quote.split = new SplitText(quote, {
						type: "lines,words,chars",
						linesClass: "split-line"
					});
					gsap.set(quote, { perspective: 400 });
					if (animation[1] == "style2") {
						gsap.set(quote.split.chars, {
							opacity: 0,
							y: "90%",
							rotateX: "-40deg"
						});
					}
					if (animation[1] == "style3") {
						gsap.set(quote.split.chars, {
							opacity: 0,
							x: "50"
						});
					}
					if (animation[1] == "style4") {
						gsap.set(quote.split.chars, {
							opacity: 0,
						});
					}
					quote.animation = gsap.to(quote.split.chars, {
					scrollTrigger: {
						trigger: quote,
						start: "top 90%",
					},
					x: "0",
					y: "0",
					rotateX: "0",
					opacity: 1,
					duration: 1,
					ease: Back.easeOut,
					stagger: .02
					});
				});
			},
		});
	}

	/*----  Sticky Header ----*/
	var pbmit_sticky_header = function () {
		if (jQuery('.pbmit-header-sticky-yes').length > 0) {
			var header_html = jQuery('#masthead .pbmit-main-header-area').html();
			jQuery('.pbmit-sticky-header').append(header_html);
			jQuery('.pbmit-sticky-header #menu-toggle').attr('id', 'menu-toggle2');
			jQuery('#menu-toggle2').on('click', function () {
				jQuery("#menu-toggle").trigger("click");
			});
			jQuery('.pbmit-sticky-header .main-navigation ul, .pbmit-sticky-header .main-navigation ul li, .pbmit-sticky-header .main-navigation ul li a').removeAttr('id');
			jQuery('.pbmit-sticky-header h1').each(function () {
				var thisele = jQuery(this);
				var thisele_class = jQuery(this).attr('class');
				thisele.replaceWith('<span class="' + thisele_class + '">' + jQuery(thisele).html() + '</span>');
			});

			// For infostack header
			if (jQuery('.pbmit-main-header-area').hasClass('pbmit-infostack-header')) {
				jQuery(".pbmit-sticky-header .pbmit-header-content").insertAfter(".pbmit-sticky-header .site-branding");
				jQuery('.pbmit-sticky-header .pbmit-header-text-box, .pbmit-sticky-header .pbmit-header-info, .pbmit-sticky-header .pbmit-mobile-search').remove();
			}
		}
	};

	var pbmit_sticky_header_class = function () {
		var lastScroll = 0;

		if (jQuery('#wpadminbar').length > 0) {
			jQuery('#masthead').addClass('pbmit-adminbar-exists');
		}

		jQuery(window).on('scroll', function () {
			var scroll = jQuery(window).scrollTop();
			var header_height = 0;

			if (jQuery('.pbmit-main-header-area').length > 0) {                
				header_height = jQuery('.pbmit-main-header-area').height();
			}

			if (scroll === 0) {
				jQuery('#masthead .pbmit-sticky-header').removeClass('pbmit-fixed-header');
			} else {
				if (scroll > lastScroll) {
					// Scrolling down → hide sticky
					jQuery('#masthead .pbmit-sticky-header').removeClass('pbmit-fixed-header');
				} else {
					// Scrolling up
					if (scroll > 300) {
						// Above 300px → show sticky
						jQuery('#masthead .pbmit-sticky-header').addClass('pbmit-fixed-header');
					} else {
						// Below 300px → hide sticky
						jQuery('#masthead .pbmit-sticky-header').removeClass('pbmit-fixed-header');
					}
				}
			}
			lastScroll = scroll;
		});
	};

	var pbmit_menu_span = function() {
		jQuery('.pbmit-max-mega-menu-override #page #site-navigation .mega-menu-wrap>ul>li.mega-menu-item .mega-sub-menu a, .pbmit-navbar ul ul a').each(function(i, v) {
			jQuery(v).contents().eq(0).wrap('<span class="pbmit-span-wrapper"/>');
		});
	}
	var pbmit_toggleSidebar = function() {
		jQuery('#menu-toggle').on('click', function() {
			jQuery("body:not(.mega-menu-pbminfotech-top) .pbmit-navbar > div, body:not(.mega-menu-pbminfotech-top)").toggleClass("active");
		})
		if (jQuery('.pbmit-navbar > div > .closepanel').length == 0) {
			jQuery('.pbmit-navbar > div').append('<span class="closepanel"><svg class="qodef-svg--close qodef-m" xmlns="http://www.w3.org/2000/svg" width="20.163" height="20.163" viewBox="0 0 26.163 26.163"><rect width="36" height="1" transform="translate(0.707) rotate(45)"></rect><rect width="36" height="1" transform="translate(0 25.456) rotate(-45)"></rect></svg>');
			jQuery('.pbmit-navbar > div > .closepanel, .mega-menu-pbminfotech-top .nav-menu-toggle').on('click', function() {
				jQuery(".pbmit-navbar > div, body, .mega-menu-wrap").toggleClass("active");
			});
			return false;
		}
	}

	/*----  Burger Menu  ----*/
	var pbmit_burger_menu = function() {
		if (jQuery('.pbmit-header-style-3').length > 0) {
			
			jQuery('.pbmit-header-style-3 .pbmit-header-overlay .main-navigation').clone().appendTo( '.pbmit-burger-menu-area-inner' ).insertBefore(".pbmit-burger-content");
			jQuery('.pbmit-burger-menu-area .main-navigation, .pbmit-burger-menu-area .main-navigation ul, .pbmit-burger-menu-area .main-navigation ul li, .pbmit-burger-menu-area .main-navigation ul li a').removeAttr('id');

			jQuery('.pbmit-burger-menu-area .main-navigation').removeClass('pbmit-navbar');
			jQuery('.pbmit-burger-menu-area .sub-menu-toggle').remove();

			jQuery('.pbmit-burger-menu-area ul.menu li:has(ul) > a').after("<span class='sub-menu-toggle'><i class='pbmit-base-icon-down-open-big'></i></span>");

			jQuery('.pbmit-burger-menu-area .sub-menu-toggle').on('click', function() {

				if (jQuery(this).siblings('.sub-menu, .children').css('display') == 'block'){			
					jQuery(this).siblings('.sub-menu, .children').slideUp();
					jQuery('i', jQuery(this)).removeClass('pbmit-base-icon-up-open-big').addClass('pbmit-base-icon-down-open-big');
				} else {
					jQuery(this).siblings('.sub-menu, .children').slideDown();
					jQuery('i', jQuery(this)).removeClass('pbmit-base-icon-down-open-big').addClass('pbmit-base-icon-up-open-big');
				}
				return false;
			});

			jQuery('.pbmit-burger-menu-link').click(function() {
				jQuery('.pbmit-burger-menu-area').addClass('show');
			});
			jQuery('.pbmit-burger-menu-area .pbmit-closepanel').click(function() {
				jQuery('.pbmit-burger-menu-area').removeClass('show');			
			});

		}
	}

	/*----  Search Btn  ----*/
	var pbmit_search_btn = function() {
		jQuery(function() {
			var search_form = jQuery(".pbmit-header-search-form");
			var search_field = jQuery('.pbmit-header-search-form .search-field');
			var $body = jQuery('body');

			jQuery(".pbmit-header-search-btn").on('click', function(e) {
				if (!search_form.hasClass('active')) {
					search_form.addClass('active');
					setTimeout(function() { search_field.get(0).focus(); }, 500);
				} else if (search_field.val() === '') {
					search_form.removeClass('active');
					search_field.get(0).focus();
				}
				e.preventDefault();
				return false;
			});

			jQuery(".pbmit-header-search-form .pbmit-search-overlay, .pbmit-header-search-form .pbmit-search-close").on('click', function (e) {
				$body.addClass('pbmit-search-animation-out');
				setTimeout(function () {
					$body.removeClass('pbmit-search-animation-out');
				}, 800);
				setTimeout(function () {
					search_form.removeClass('active');
				}, 800);
				e.preventDefault();
				return false;
			});
		});
	}

	/*----  Sticky Sidebar  ----*/
	var pbmit_thia_sticky = function() {
		if(typeof jQuery.fn.theiaStickySidebar == "function"){
			jQuery('.pbmit-sticky-sidebar').theiaStickySidebar({
				additionalMarginTop: 120
			});
			jQuery('.pbmit-sticky-column').theiaStickySidebar({
				additionalMarginTop: 180
			});
		}
	}

	/*----  Sortable  ----*/
	var pbmit_sorting = function() {
		jQuery('.pbmit-sortable-yes:not(.pbmit-ajax-sortable-yes)').each(function() {
			var boxes = jQuery('.pbmit-element-posts-wrapper', this);
			var links = jQuery('.pbmit-sortable-list a', this);
			boxes.isotope({
				animationEngine: 'best-available',
				layoutMode: 'masonry',
				masonry: {
					horizontalOrder: true
				}
				
			});
			links.on('click', function(e) {
				var selector = jQuery(this).data('sortby');
				if (selector != '*') {
					var selector = '.' + selector;
				}
				boxes.isotope({
					animationEngineString : 'best-available',
					filter: selector,
					itemSelector: '.pbmit-ele',
					layoutMode: 'masonry',
					masonry: {
						horizontalOrder: true
					}
				});
				links.removeClass('pbmit-selected');
				jQuery(this).addClass('pbmit-selected');
				e.preventDefault();
			});
		});
	}

	/*----  Active Hover  ----*/
	var pbmit_active_hover = function() {
		var pbmit_var = jQuery('.pbmit-element-static-box-style-1, .pbmit-element-static-box-style-2, .pbmit-element-portfolio-style-2 ,.pbmit-element-service-style-3, .pbmit-element-miconheading-style-7');
		if (!pbmit_var.length) {
			return;
		}
		pbmit_var.each(function() {
			var pbmit_Class = '.pbmit-static-box-style-1, .pbmit-hover-inner .pbmit-title-wrapper, .pbmit-portfolio-style-2, .pbmit-hover-inner li, .pbmit-miconheading-style-7';
			jQuery(this)
				.find(pbmit_Class).first()
				.addClass('pbmit-active');
			jQuery(this)
				.find(pbmit_Class)
				.on('mouseover', function() {
					jQuery(this).addClass('pbmit-active').siblings().removeClass('pbmit-active');
				});
		});
	}

	/* Static Box Slider */
	var pbmit_staticbox_hover_slide = function() {
		if (typeof Swiper !== 'undefined') {
			var pbmit_hover = new Swiper(".pbmit-static-image", {
				speed: 6000,
				effect: 'fade',
				allowTouchMove: false
			});
			jQuery('.pbmit-hover-inner li').on('mouseover', function(e) {
				e.preventDefault();
				var myindex = jQuery(this).index();
				pbmit_hover.slideTo(myindex, 1000, false);
			});		
		}
	}

	/*----  Active Hover Pricing  ----*/
	var pbmit_active_hover_pricing = function() {
		var pbmit_var = jQuery('.pbminfotech-ele-ptable-style-2');
		if (!pbmit_var.length) {
			return;
		}
		pbmit_var.each(function() {
			var pbmit_Class = '.pbmit-ptable-col';
			jQuery(this)
				.find(pbmit_Class).first()
				.addClass('pbmit-active');
			jQuery(this)
				.find(pbmit_Class)
				.on('click', function() {
					jQuery(this).addClass('pbmit-active').siblings().removeClass('pbmit-active');
				});
		});
	}

	/*----  Active Hover Service  ----*/
	var pbmit_active_hover_service = function() {
		var pbmit_var = jQuery('.pbmit-element-service-style-4');

		if (!pbmit_var.length) {
			return;
		}

		pbmit_var.each(function() {

			var pbmit_Class = '.pbmit-service-style-4';

			// Make first item active by default
			jQuery(this)
				.find(pbmit_Class)
				.first()
				.addClass('pbmit-active');

			// Activate on hover
			jQuery(this)
				.find(pbmit_Class)
				.on('mouseenter', function() {
					jQuery(this)
						.addClass('pbmit-active')
						.siblings()
						.removeClass('pbmit-active');
				});

		});
	}

	/*----  Tween Effect  ----*/
	var pbmit_tween_effect = function() {
		if (jQuery(window).width() < 768) return;

		jQuery(window).on('scroll resize', function () {
			jQuery('.pbmit-tween-effect').each(function () {
			let $el = jQuery(this),
				rect = this.getBoundingClientRect(),
				inView = rect.top < window.innerHeight && rect.bottom > 0;

			if (!inView) return;

			let progress = 1 - (rect.top / window.innerHeight);
			progress = Math.max(0, Math.min(1, progress)); // Clamp 0–1

			const getVal = (attr) => parseFloat($el.data(attr)) || 0;

			let tx = getVal('x-start') + (getVal('x-end') - getVal('x-start')) * progress,
				ty = getVal('y-start') + (getVal('y-end') - getVal('y-start')) * progress,
				scale = getVal('scale-x-start') + (getVal('scale-x-end') - getVal('scale-x-start')) * progress,
				skewX = getVal('skew-x-start') + (getVal('skew-x-end') - getVal('skew-x-start')) * progress,
				skewY = getVal('skew-y-start') + (getVal('skew-y-end') - getVal('skew-y-start')) * progress,
				rotate = getVal('rotate-x-start') + (getVal('rotate-x-end') - getVal('rotate-x-start')) * progress;

			$el.css('transform', `translate(${tx}%, ${ty}%) scale(${scale}) skew(${skewX}deg, ${skewY}deg) rotate(${rotate}deg)`);
			});
		}).trigger('scroll');
	}

	/*----  Tabs  ----*/
	var pbmit_tabs_element = function() {
		var tab_number = '';
		jQuery('.pbmit-tab-link').on('click', function(){
			if( !jQuery(this).hasClass('pbmit-tab-li-active') ){
				var parent = jQuery(this).closest('ul.pbmit-tabs-links');
				jQuery( 'li', parent).each(function(){
					jQuery(this).removeClass('pbmit-tab-li-active')
				});
				jQuery(this).addClass('pbmit-tab-li-active');
				tab_number = jQuery( this ).data('pbmit-tab');
				jQuery(this).parent().parent().find('.pbmit-tab-content').removeClass('pbmit-tab-active');
				jQuery(this).parent().parent().find('.pbmit-tab-content-'+tab_number).addClass('pbmit-tab-active');
			}
		});
		var this_title = '';
		jQuery('.pbmit-tab-content-title').on('click', function(){
			this_title = jQuery(this);
			tab_number = jQuery( this ).data('pbmit-tab');
			jQuery( this ).closest('.pbmit-tabs').find('li.pbmit-tab-link[data-pbmit-tab="'+tab_number+'"]',  ).trigger('click');
			var animateTo = jQuery(this_title).offset().top - 10;
			if (jQuery('#wpadminbar').length > 0) {
				animateTo = animateTo - jQuery('#wpadminbar').height();
			}
			jQuery('html, body').animate({
				scrollTop: animateTo
			}, 500);
		});
	};

	/*----  Video Popup  ----*/
	var pbmit_video_popup = function() {
		jQuery('.pbmit-popup').on('click', function(event) {
			event.preventDefault();
			var href = jQuery(this).attr('href');
			var title = jQuery(this).attr('title');
			window.open(href, title, "width=600,height=500");
		});
	}

	/*----  Card Verticel Pinning  ----*/
	function pbmit_card_verticel_pinning() {
		var pbmit_var = jQuery('.pbmit-element-card-box-style-1');
		if (!pbmit_var.length) {
			return;
		}
		ScrollTrigger.matchMedia({
			"(min-width: 992px)": function() {

				let pbmitpanels = gsap.utils.toArray(".pbmit-element-card-box-style-1 .pbmit-card-box-wrapper");
				const spacer = 25;
			
				let pbmitheight = pbmitpanels[0].offsetHeight + 70;
				pbmitpanels.forEach((pbmitpanel, i) => {
				ScrollTrigger.create({
					trigger: pbmitpanel, 
					start: () => `top ${100 + (i * spacer)}px`, 
					endTrigger: '.pbmit-element-card-box-style-1', 
					end: `bottom top+=${pbmitheight + (pbmitpanels.length * spacer)}`,
					pin: true, 
					pinSpacing: false, 
				});
				});
			},
			"(max-width:992px)": function() {
				ScrollTrigger.getAll().forEach(pbmitpanels => pbmitpanels.kill(true));
			}
		});
	}

	ScrollTrigger.matchMedia({
		"(max-width: 1200px)": function() {
			ScrollTrigger.getAll().forEach(t => t.kill());
		}
	});

	// on load
	jQuery(window).on('load', function(){
		pbmit_title_animation();
		pbmit_sticky_header();
		pbmit_sticky_header_class();
		pbmit_menu_span();
		pbmit_toggleSidebar();
		pbmit_burger_menu();
		pbmit_search_btn();
		pbmit_thia_sticky();
		pbmit_sorting();
		pbmit_active_hover();
		pbmit_staticbox_hover_slide();
		pbmit_active_hover_pricing();
		pbmit_active_hover_service();
		pbmit_tween_effect();
		pbmit_tabs_element();
		pbmit_video_popup();
		pbmit_card_verticel_pinning();
		gsap.delayedCall(1, () =>
			ScrollTrigger.getAll().forEach((t) => {
				t.refresh();
			})
		);
	});
})($);