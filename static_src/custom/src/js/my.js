// fix header
document.addEventListener("DOMContentLoaded", function(event) {
	if (document.documentElement.scrollTop > 0) {
		header.classList.add('header__scrolled');
	}

	window.addEventListener("scroll", function (e) {
		let header = document.getElementById('header');
		if (window.scrollY > 0) {
			header.classList.add('header__scrolled');		
		} else {
			header.classList.remove('header__scrolled');
		}
	}); 
  });

// смена языка
// let lang_textHeader = document.querySelector('.header-lang__text');
// let lang_bodyHeader = document.querySelector('.header-lang');
// lang_textHeader.addEventListener("click", function (e) {
// 	lang_bodyHeader.classList.toggle('is-active');
// });
// document.documentElement.addEventListener("click", function (e) {
// 	if (!e.target.closest('.header-lang')) {
// 		lang_bodyHeader.classList.remove('is-active');
// 	}
// });

// if (document.querySelector('.footer')) {
// 	let lang_textFooter = document.querySelector('.header-lang__text-footer');
// 	let lang_bodyFooter = document.querySelector('.header-lang-footer');
// 	lang_textFooter.addEventListener("click", function (e) {
// 		lang_bodyFooter.classList.toggle('is-active');
// 	});
// 	document.documentElement.addEventListener("click", function (e) {
// 		if (!e.target.closest('.header-lang-footer')) {
// 			lang_bodyFooter.classList.remove('is-active');
// 		}
// 	});
// }

//бегущая строка
$(function ($, undefined) {
	$('.country__content--top').eocjsNewsticker({
		'speed': 25,
		'timeout': 0.5,
		'divider': '',
	});
});

$(function ($, undefined) {
	$('.country__content--bottom').eocjsNewsticker({
		'speed': 25,
		'timeout': 0.5,
		'divider': '',
		'direction': 'rtl'
	});
});

// анимация товара
$(".just-scan__images").brazzersCarousel();

// фильтер shop моб
$('.button-filter').on('click', function () {
	$('body').addClass('scroll-no')
	$('.modal-filter[data-modal="content-filter"]').addClass('active')
})

$('.button-sort').on('click', function () {
	$('body').addClass('scroll-no')
	$('.modal-filter[data-modal="content-sort"]').addClass('active')
})

$('.modal-filter svg').on('click', function () {
	$('body').removeClass('scroll-no')
	$('.modal-filter').removeClass('active')
})

//// показать еще
//$('.show__more a').on('click', function (e) {
//	e.preventDefault()
//	$('.shop__items.close').addClass('open')
//})

// при наведений на цвет смена товара
let img_url = ''
let active_color_img = true
$('.color-select__item i').on('click', function (e) {
	e.preventDefault()
	active_color_img = false
	$(this).parents('.color-select__list').find('i').removeClass('color-select__btn--active')
	$(this).addClass('color-select__btn--active')
	$(this).parents('.shop__item').find('img').attr('src', $(this).attr('data-url'))
	$(this).parents('.shop__item').attr('href', $(this).attr('data-product-url'))
	$(this).parents('.shop__item').attr('title', $(this).attr('data-product-title'))
})

//$('.color-select__item i').hover(
//	function () {
//		img_url = $(this).parents('.shop__item').find('img').attr('src')
//		$(this).parents('.shop__item').find('img').attr('src', $(this).attr('data-url'))
//	},
//	function () {
//		if (active_color_img) {
//			$(this).parents('.shop__item').find('img').attr('src', img_url)
//		}
//	}
//)

// показать еще
$('.cart__more-btn').click(function () {
	$('.cart__more-text--hide').slideToggle(function(){
		$('.cart__more-btn').toggleClass("active", function(){
			if ($('.cart__more-btn').hasClass('active')){
				$('.cart__more-btn').text($('.cart__more-btn').attr('data-hide'));
			} else{
				$('.cart__more-btn').text($('.cart__more-btn').attr('data-show'));
			}
		});
	});
	// if ($('.cart__more-btn').text() == "Скрыть") {
	// 	$(this).text("Показать еще")
	// } else {
	// 	$(this).text("Скрыть")
	// }
});


// степпер цены
$(document).ready(function () {
	$('.minus').click(function () {
		let $input = $(this).parent().find('input');
		let count = parseInt($input.val()) - 1;
		count = count < 1 ? 1 : count;
		$input.val(count);
		$input.change();
		return false;
	});
	$('.plus').click(function () {
		let $input = $(this).parent().find('input');
		$input.val(parseInt($input.val()) + 1);
		$input.change();
		return false;
	});
});

// моб версия-поиск
if (document.querySelector('.menu__item-search')) {
	var menuSearch = document.querySelector('.menu__search-icon');
	var headerContent = document.querySelector('.header__content');
	menuSearch.addEventListener("click", function (e) {
		headerContent.classList.toggle('active');
	});
	document.documentElement.addEventListener("click", function (e) {
		if (!e.target.closest('.header__content')) {
			headerContent.classList.remove('active');
		}
	});
}

// пк версия-поиск
if (document.querySelector('.menu__search-icon')) {
	document.addEventListener('DOMContentLoaded', function () {
		var menuItemSearch = document.querySelector('.menu__item-search');
		var menuItemSearchInput = document.querySelector('.menu__item-search input');

		menuItemSearch.addEventListener('mouseenter', function (e) {
			menuItemSearchInput.classList.add('menu__item-input');
		});
		menuItemSearch.addEventListener('mouseleave', function () {
			menuItemSearchInput.classList.remove('menu__item-input');
		})
	})
}

// фильтр
jQuery(function ($) {
	$('.shop .shop__select .selectric').on('click', function () {
		$('.modal-select').addClass('open')
		$(`.shop__filter-content.show .selectric-wrapper`).removeClass('selectric-hover selectric-open')
		$(`.shop__filter-content .selectric-wrapper[data-type='${$(this).attr('data-type')}']`).addClass('selectric-hover selectric-open')
	})

	$('.modal-select .selectric').on('click', function () {
		if ($(`.shop__filter-content .selectric-wrapper[data-type='${$(this).attr('data-type')}']`).hasClass('selectric-open')) {
			$(`.shop__filter-content .selectric-wrapper[data-type='${$(this).attr('data-type')}']`).removeClass('selectric-hover selectric-open')
		} else {
			$(`.shop__filter-content .selectric-wrapper[data-type='${$(this).attr('data-type')}']`).addClass('selectric-hover selectric-open')
		}
		let bool = true
		let selects = Array.from($(`.shop__filter-content .selectric-wrapper`))
		selects.forEach((e) => {
			if ($(e).hasClass('selectric-open')) {
				bool = false
			}
		})
		if (bool) {
			$('.modal-select').removeClass('open')
		}
	})

	$('.modal-select__bg').on('click', function () {
		$('.modal-select').removeClass('open')
	})

	$('.facet li').on('click', function(){
		// Click on facet value handler
		window.location.href = $(this).find('a').attr('href');
	})

	$('.sort li').on('click', function(){
		// Click on sort option handler
		$(this).closest('form').submit();
	})
})

// 404 paint
if (document.querySelector('.paint')) {
	var cvets = ['#ff7c2a','#9d2b2e','#115e67'];
	var $i=0;

	var cvet = cvets[$i];
	var $canvas = $('.p5Canvas');
	let img;
	setTimeout(function (){
		$(document).dblclick(function(event) {
			switch (event.which) {
				case 1:
					$i++;
					$('.p5Canvas').css('cursor',`url(static/custom/build/img/cursor-${$i}.png), none`);
					cvet = cvets[$i];
					if ($i===3){
						$i=0;
						cvet = cvets[$i];
						$('.p5Canvas').css('cursor',`url(static/custom/build/img/cursor-${$i}.png), none`);
					}
			}
		});
	},100);

	function preload() {
		img = loadImage('/static/custom/build/img/paint-404.jpg');
	}

	function setup() {

		var can = createCanvas(685, 319);
		can.center('horizontal');
		image(img, 0, 0);
		can.parent('#paint');
	}

	function draw() {
		stroke(cvet);
		strokeWeight(4);

		if (mouseIsPressed === true) {

			line(mouseX, mouseY, pmouseX, pmouseY);

		}
	}
}
