if (document.querySelector('.canvas-hero-block')) {

    var screenHeight = window.innerHeight;
    var Canvas_offset = $('.canvas-hero-block').offset().top;
    var CanvasEnd_offset = $('#canvas-hero-end').offset().top;
    var Canvas_items_stack = $('.canvas-hero-block').find("[class^=item]");
    var Canvas_step = $('.canvas-hero-block').innerHeight() / Canvas_items_stack.length;
    var Canvas_crd = [];

    for (let index = 0; index < Canvas_items_stack.length; index++) {
        Canvas_crd[index] = index == 0 ? Canvas_offset + Canvas_step : Canvas_step + Canvas_crd[index - 1];
    }

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > Canvas_offset &&
            $(window).scrollTop() + window.innerHeight < CanvasEnd_offset) {

            for (let index = 0; index < Canvas_crd.length; index++) {
                if ($(document).scrollTop() < Canvas_crd[index]) {
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

if (document.querySelector('.weare')) {

    var Weare_offset = $('#weare').offset().top;
    var WeareEnd_offset = $('#weare-end').offset().top;
    var Weare_items_stack = $('#weare').find("[class^=item]");
    var Weare_step = $('#weare').innerHeight() / Weare_items_stack.length;
    var Weare_crd = [];


    for (let index = 0; index < Weare_items_stack.length; index++) {
        Weare_crd[index] = index == 0 ? Weare_offset + Weare_step : Weare_step + Weare_crd[index - 1];
    }

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > Weare_offset &&
            $(window).scrollTop() + window.innerHeight < WeareEnd_offset) {

            for (let index = 0; index < Weare_crd.length; index++) {
                if ($(document).scrollTop() < Weare_crd[index]) {
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

function show_text_on_home_banner(banner_id) {
    let wrapper_id = banner_id;
    if ($(document).scrollTop() > $(wrapper_id).offset().top){
        $(wrapper_id).find('.item-0').addClass('element-show');
    }    
}

if (document.querySelector('.why')) {

    var Why_offset = $('#why').offset().top;
    var WhyEnd_offset = $('#why-end').offset().top;
    var Why_items_stack = $('#why').find("[class^=item]");
    var Why_step = $('#why').innerHeight() / Why_items_stack.length;
    var Why_crd = [];

    for (let index = 0; index < Why_items_stack.length; index++) {
        Why_crd[index] = index == 0 ? Why_offset + Why_step : Why_step + Why_crd[index - 1];
    }

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > Why_offset &&
            $(window).scrollTop() + window.innerHeight < WhyEnd_offset) {

            // $('.be-bigger__title').css({
            //     color: $(be_bigger_items_stack[index]).attr('data-color')
            // });

            for (let index = 0; index < Why_crd.length; index++) {
                if ($(document).scrollTop() < Why_crd[index]) {


                    $('.why__title').css({
                        color: $($('.why').find(`[class^=item]`)[index]).attr('data-color')
                    });

                    $('.why__subtitle').css({
                        color: $($('.why').find(`[class^=item]`)[index]).attr('data-color')
                    });

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