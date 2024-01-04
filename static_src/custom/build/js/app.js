	// Menu burger
	const iconMenu = document.querySelector('.menu__icon');
	const menuBody = document.querySelector('.menu__body');
	const menuTop = document.querySelector('.header__content');
	if (iconMenu) {
		iconMenu.addEventListener("click", function (e) {
			document.body.classList.toggle('lock');
			iconMenu.classList.toggle('active');
			menuBody.classList.toggle('active');
			menuTop.classList.toggle('fixed-menu');
		});
	}

// Importing CanvasScrollHero
// Logging
const logContainer = document.getElementById('comments');
const log = text => {
    if (logContainer) {
        logContainer.innerHTML += text + '\n';
    } else {
        console.log(text);
    }
};

// Loading indicator
const startProgress = () => {
    document.documentElement.classList.add('cursor-loading');
};

const stopProgress = () => {
    document.documentElement.classList.remove('cursor-loading');
};

// average over an array
const average = arr => {
    return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2);
};

// promise with timeout
const withTimeout = async (promise, timeout) => {
    return new Promise(async (resolve, reject) => {
        setTimeout(() => {
            reject(`Promise ${promise} timed out at ${timeout}ms`);
        }, timeout);

        await promise;
        resolve(promise);
    });
};

// Importing other js files
function initSliderCart() {
	new Swiper('.cart__swiper', {
		loop: true,
		pagination: {
			el: '.swiper-pagination',
			clickable: true
		},
		autoplay: {
			delay: 2500,
		},
	});
}

function detectDeviceCart() {
	if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
		// true for mobile device
		initSliderCart();
	} else {
		// false for not mobile device
	}
}
detectDeviceCart();

function initSliderLike() {
	new Swiper('.like__swiper', {
		slidesPerView: 1,
		loop: true,
		pagination: {
			el: '.swiper-pagination',
			clickable: true
		},
		autoplay: {
			delay: 2500,
		},
		breakpoints: {
			768: {
				slidesPerView: 2,
			},
		},
	});
}

function detectDeviceLike() {
	if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
		// true for mobile device
		initSliderLike();
	} else {
		// false for not mobile device
	}
}
detectDeviceLike();
var move_array = [];
var move_objects = document.querySelectorAll("[data-move]");

if (move_objects.length > 0) {
	for (var _index10 = 0; _index10 < move_objects.length; _index10++) {
		var _el6 = move_objects[_index10];

		var data_move = _el6.getAttribute("data-move");

		if (data_move != "" || data_move != null) {
			_el6.setAttribute("data-move-index", _index10);

			move_array[_index10] = {
				parent: _el6.parentNode,
				index: index_in_parent(_el6)
			};
		}
	}
}

function dynamic_adapt() {
	var w = document.querySelector("body").offsetWidth;

	if (move_objects.length > 0) {
		for (var _index11 = 0; _index11 < move_objects.length; _index11++) {
			var _el7 = move_objects[_index11];

			var _data_move = _el7.getAttribute("data-move");

			if (_data_move != "" || _data_move != null) {
				var data_array = _data_move.split(",");

				var data_parent = document.querySelector("." + data_array[0]);
				var data_index = data_array[1];
				var data_bp = data_array[2];

				if (w < data_bp) {
					if (!_el7.classList.contains("js-move_done_" + data_bp)) {
						if (data_index > 0) {
							//insertAfter
							var actual_index = index_of_elements(data_parent)[data_index];
							data_parent.insertBefore(_el7, data_parent.childNodes[actual_index]);
						} else {
							data_parent.insertBefore(_el7, data_parent.firstChild);
						}

						_el7.classList.add("js-move_done_" + data_bp);
					}
				} else {
					if (_el7.classList.contains("js-move_done_" + data_bp)) {
						dynamic_adaptive_back(_el7);

						_el7.classList.remove("js-move_done_" + data_bp);
					}
				}
			}
		}
	}
}

function dynamic_adaptive_back(el) {
	var index_original = el.getAttribute("data-move-index");
	var move_place = move_array[index_original];
	var parent_place = move_place["parent"];
	var index_place = move_place["index"];

	if (index_place > 0) {
		//insertAfter
		var actual_index = index_of_elements(parent_place)[index_place];
		parent_place.insertBefore(el, parent_place.childNodes[actual_index]);
	} else {
		parent_place.insertBefore(el, parent_place.firstChild);
	}
}

function index_in_parent(node) {
	var children = node.parentNode.childNodes;
	var num = 0;

	for (var _i2 = 0; _i2 < children.length; _i2++) {
		if (children[_i2] == node) return num;
		if (children[_i2].nodeType == 1) num++;
	}

	return -1;
}

function index_of_elements(parent) {
	var children = [];

	for (var _i3 = 0; _i3 < parent.childNodes.length; _i3++) {
		if (parent.childNodes[_i3].nodeType == 1 && parent.childNodes[_i3].getAttribute("data-move") == null) {
			children.push(_i3);
		}
	}
	return children;
}

window.addEventListener("resize", function (event) {
	dynamic_adapt();
});
dynamic_adapt();
$(function () {
	$('select').selectric();
});
// ./tabs.js
if (document.querySelector('.be-bigger')) {

    var be_bigger_items_stack = $('.be-bigger').find('.be-bigger__item'); // список контейнеров с фото справа
    var be_bigger_offset = $('.be-bigger').offset().top;
    var be_bigger_step = ($('#be-bigger-end').offset().top - window.innerHeight) / be_bigger_items_stack.length;
    var be_bigger_crd = [];

    //////// Обработчик изменения цвета надписи в be-bigger блоке ///////////
    for (let index = 0; index < be_bigger_items_stack.length; index++) {
        be_bigger_crd[index] = index == 0 ? be_bigger_step : be_bigger_step + be_bigger_crd[index - 1];
    }

    $(window).on('scroll', function () {
        for (let index = 0; index < be_bigger_crd.length; index++) {
            if ($(document).scrollTop() < be_bigger_offset + be_bigger_crd[index]) {


                $('.be-bigger__title').css({
                    color: $(be_bigger_items_stack[index]).attr('data-color')
                });

                $('#be-bigger').find(`[class^=item]:not(.item-${index})`).removeClass('element-show');
                if ($('#be-bigger').find(`.item-${index}`).removeClass('element-show')){
                    $('#be-bigger').find(`.item-${index}`).addClass('element-show');
                }
                break;
            }
        }
    })
}

if (document.querySelector('.attract')) {

    var Attract_offset = $('#attract').offset().top;
    var AttractEnd_offset = $('#attract-end').offset().top;
    var Attract_items_stack = $('#attract').find("[class^=item]");
    var Attract_step = $('#attract').innerHeight() / Attract_items_stack.length;
    var Attract_crd = [];

    for (let index = 0; index < Attract_items_stack.length; index++) {
        Attract_crd[index] = index == 0 ? Attract_offset + Attract_step : Attract_step + Attract_crd[index - 1];
    }

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > Attract_offset &&
            $(window).scrollTop() + window.innerHeight < AttractEnd_offset) {
            for (let index = 0; index < Attract_crd.length; index++) {
                if ($(document).scrollTop() < Attract_crd[index]) {
                    $('.block-scroll').find(`[class^=item]:not(.item-${index})`).removeClass('element-show');
                    if ($('.block-scroll').find(`.item-${index}`).removeClass('element-show')){
                        $('.block-scroll').find(`.item-${index}`).addClass('element-show');
                    }
                    break;
                }
            }

        }
    })
}
var languageSwitcher = {

    /**
     * Init language switcher in header
     */
    init_header: function () {
        let lang_textHeader = document.querySelector('.header-lang__text');
        let lang_bodyHeader = document.querySelector('.header-lang');
        lang_textHeader.addEventListener("click", function (e) {
            lang_bodyHeader.classList.toggle('is-active');
        });
        document.documentElement.addEventListener("click", function (e) {
            if (!e.target.closest('.header-lang')) {
                lang_bodyHeader.classList.remove('is-active');
            }
        });
    },

    /**
     * Init language switcher in footer
     */
    init_footer: function () {
        if (document.querySelector('.footer')) {
            let lang_textFooter = document.querySelector('.header-lang__text-footer');
            let lang_bodyFooter = document.querySelector('.header-lang-footer');
            lang_textFooter.addEventListener("click", function (e) {
                lang_bodyFooter.classList.toggle('is-active');
            });
            document.documentElement.addEventListener("click", function (e) {
                if (!e.target.closest('.header-lang-footer')) {
                    lang_bodyFooter.classList.remove('is-active');
                }
            });
        }
    }
}
/*global jQuery */

;(function($, o={}) {
    o.basket = {
        is_form_being_submitted: false,
        init: function(options) {
            if (typeof options == 'undefined') {
                options = {'basketURL': document.URL};
            }
            o.basket.url = options.basketURL || document.URL;
            $('#content_inner').on('click', '#basket_formset a[data-behaviours~="remove"]', function(event) {
                o.basket.checkAndSubmit($(this), 'form', 'DELETE');
                event.preventDefault();
            });

            $('#content_inner').on('click', '[data-counter=plus], [data-counter=minus]', function(){
                let input = $(this).parent().find('input');
                let current_value = parseInt(input.val());
                let step = $(this).data('counter') === 'plus' ? 1: -1;
                let new_value = current_value + step;
                if (new_value < 1){
                    new_value = 1;
                }
                // else if (new_value > max_value){
                //     new_value = max_value;
                // }
                input.val(new_value);
                $(this).closest('#basket_formset').submit();

                return false;
            });

            $('#content_inner').on('submit', '#basket_formset', o.basket.submitBasketForm);
        },
        submitBasketForm: function(event) {
            $('#messages').html('');
            var payload = $('#basket_formset').serializeArray();
            $.post(o.basket.url, payload, o.basket.submitFormSuccess, 'json');
            if (event) {
                event.preventDefault();
            }
        },
        submitFormSuccess: function(data) {
            $('#content_inner').html(data.content_html);
            $('.mini-basket-ajax').html(data.mini_basket_html);
            $('select').selectric();

            // Show any flash messages
            o.messages.clear();
            for (var level in data.messages) {
                for (var i=0; i<data.messages[level].length; i++) {
                    o.messages[level](data.messages[level][i]);
                }
            }
            o.basket.is_form_being_submitted = false;
        },
        checkAndSubmit: function($ele, formPrefix, idSuffix) {
            if (o.basket.is_form_being_submitted) {
                return;
            }
            var formID = $ele.attr('data-id');
            var inputID = '#id_' + formPrefix + '-' + formID + '-' + idSuffix;
            $(inputID).attr('checked', 'checked');
            $ele.closest('form').submit();
            o.basket.is_form_being_submitted = true;
        }
    };

    o.checkout = {
        gateway: {
            init: function () {
                var radioWidgets = $('form input[name=options]');
                var selectedRadioWidget = $('form input[name=options]:checked');
                o.checkout.gateway.handleRadioSelection(selectedRadioWidget.val());
                radioWidgets.change(o.checkout.gateway.handleRadioChange);
                $('#id_username').focus();
            },
            // handleRadioChange: function () {
            //     o.checkout.gateway.handleRadioSelection($(this).val());
            // },
            // handleRadioSelection: function (value) {
            //     var pwInput = $('#id_password');
            //     if (value == 'anonymous' || value == 'new') {
            //         pwInput.attr('disabled', 'disabled');
            //     } else {
            //         pwInput.removeAttr('disabled');
            //     }
            // }
        }
    };

    // Replicate Django's flash messages so they can be used by AJAX callbacks.
    o.messages = {
        addMessage: function(tag, msg) {
            var msgHTML = '<div class="alert alert-dismissible fade show alert-' + tag + '">' +
                '<a href="#" class="close" data-dismiss="alert">&times;</a>'  + msg +
                '</div>';
            $('#messages').append($(msgHTML));
        },
        debug: function(msg) { o.messages.addMessage('debug', msg); },
        info: function(msg) { o.messages.addMessage('info', msg); },
        success: function(msg) { o.messages.addMessage('success', msg); },
        warning: function(msg) { o.messages.addMessage('warning', msg); },
        error: function(msg) { o.messages.addMessage('danger', msg); },
        clear: function() {
            $('#messages').html('');
        },
        scrollTo: function() {
            $('html').animate({scrollTop: $('#messages').offset().top});
        },
        closeAlert: function(e){
            $('body').on('click', '.alert a.close', function(e){
                e.preventDefault();
                $(this).closest('.alert').remove();
            })
        },
        init: function(){
            o.messages.closeAlert();
        }
    };

    o.init = function(){
        o.messages.init();
    }
})(jQuery, window.oscar = window.oscar || {});

$(document).ready(function() {
    oscar.init();
});

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


// // степпер цены
// $(document).ready(function () {
// 	$('.minus').click(function () {
// 		let $input = $(this).parent().find('input');
// 		let count = parseInt($input.val()) - 1;
// 		count = count < 1 ? 1 : count;
// 		$input.val(count);
// 		$input.change();
// 		return false;
// 	});
// 	$('.plus').click(function () {
// 		let $input = $(this).parent().find('input');
// 		$input.val(parseInt($input.val()) + 1);
// 		$input.change();
// 		return false;
// 	});
// });

$(document).ready(function(){
	languageSwitcher.init_header();
	languageSwitcher.init_footer();
})

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