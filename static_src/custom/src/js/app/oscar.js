;(function(o={}, $) {
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
                let new_value = current_value + step
                if (new_value < 1) new_value = 1;
                input.val(new_value);
                $(this).closest('#basket_formset').submit();

                return false;
            });

            $('#content_inner').on('submit', '#basket_formset', o.basket.submitBasketForm);
        },
        submitBasketForm: function(event) {
            // $('#messages').html('');
            var payload = $('#basket_formset').serializeArray();
            $.post(o.basket.url, payload, o.basket.submitFormSuccess, 'json');
            if (event) {
                event.preventDefault();
            }
        },
        submitFormSuccess: function(data) {
            $('#content_inner').html(data.content_html);
            $('select').selectric();
            //
            // // Show any flash messages
            // o.messages.clear();
            // for (var level in data.messages) {
            //     for (var i=0; i<data.messages[level].length; i++) {
            //         o.messages[level](data.messages[level][i]);
            //     }
            // }
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

    // Replicate Django's flash messages so they can be used by AJAX callbacks.
    // o.messages = {
    //     addMessage: function(tag, msg) {
    //         var msgHTML = '<div class="alert alert-dismissible fade show alert-' + tag + '">' +
    //             '<a href="#" class="close" data-dismiss="alert">&times;</a>'  + msg +
    //             '</div>';
    //         $('#messages').append($(msgHTML));
    //     },
    //     debug: function(msg) { o.messages.addMessage('debug', msg); },
    //     info: function(msg) { o.messages.addMessage('info', msg); },
    //     success: function(msg) { o.messages.addMessage('success', msg); },
    //     warning: function(msg) { o.messages.addMessage('warning', msg); },
    //     error: function(msg) { o.messages.addMessage('danger', msg); },
    //     clear: function() {
    //         $('#messages').html('');
    //     },
    //     scrollTo: function() {
    //         $('html').animate({scrollTop: $('#messages').offset().top});
    //     }
    // };
})(window.oscar = window.oscar || {}, jQuery);