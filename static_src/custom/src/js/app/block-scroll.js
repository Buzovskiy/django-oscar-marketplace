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