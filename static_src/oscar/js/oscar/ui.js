/*global jQuery */

var oscar = (function(o, $) {
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
        }
    };

    o.search = {
        init: function() {
            o.search.initSortWidget();
            o.search.initFacetWidgets();
        },
        initSortWidget: function() {
            // Auto-submit (hidden) search form when selecting a new sort-by option
            $('#id_sort_by').on('change', function() {
                $(this).closest('form').submit();
            });
        },
        initFacetWidgets: function() {
            // Bind events to facet checkboxes
            $('.facet_checkbox').on('change', function() {
                window.location.href = $(this).nextAll('.facet_url').val();
            });
        }
    };

    // Notifications inbox within 'my account' section.
    o.notifications = {
        init: function() {
            $('a[data-behaviours~="archive"]').click(function() {
                o.notifications.checkAndSubmit($(this), 'archive');
            });
            $('a[data-behaviours~="delete"]').click(function() {
                o.notifications.checkAndSubmit($(this), 'delete');
            });
        },
        checkAndSubmit: function($ele, btn_val) {
            $ele.closest('tr').find('input').attr('checked', 'checked');
            $ele.closest('form').find('button[value="' + btn_val + '"]').click();
            return false;
        }
    };

    // Site-wide forms events
    o.forms = {
        init: function() {
            // Forms with this behaviour are 'locked' once they are submitted to
            // prevent multiple submissions
            $('form[data-behaviours~="lock"]').submit(o.forms.submitIfNotLocked);

            // Disable buttons when they are clicked and show a "loading" message taken from the
            // data-loading-text attribute.
            // Do not disable if button is inside a form with invalid fields.
            // This uses a delegated event so that it keeps working for forms that are reloaded
            // via AJAX: https://api.jquery.com/on/#direct-and-delegated-events
            $(document.body).on('click', '[data-loading-text]', function(){
                var $btn_or_input = $(this),
                    form = $btn_or_input.parents("form");
                if (!form || $(":invalid", form).length == 0) {
                    var d = 'disabled',
                        val = $btn_or_input.is('input') ? 'val' : 'html';
                    // push to event loop so as not to delay form submission
                    setTimeout(function() {
                        $btn_or_input[val]($btn_or_input.data('loading-text'));
                        $btn_or_input.addClass(d).attr(d, d).prop(d, true);
                    });
                }
            });
            // stuff for star rating on review page
            // show clickable stars instead of a select dropdown for product rating
            var ratings = $('.reviewrating');
            if(ratings.length){
                ratings.find('.star-rating i').on('click',o.forms.reviewRatingClick);
            }
        },
        submitIfNotLocked: function() {
            var $form = $(this);
            if ($form.data('locked')) {
                return false;
            }
            $form.data('locked', true);
        },
        reviewRatingClick: function(){
            var ratings = ['One','Two','Three','Four','Five']; //possible classes for display state
            $(this).parent().removeClass('One Two Three Four Five').addClass(ratings[$(this).index()]);
            $(this).closest('.controls').find('select').val($(this).index() + 1); //select is hidden, set value
        }
    };

    o.checkout = {
        gateway: {
            init: function() {
                var radioWidgets = $('form input[name=options]');
                var selectedRadioWidget = $('form input[name=options]:checked');
                o.checkout.gateway.handleRadioSelection(selectedRadioWidget.val());
                radioWidgets.change(o.checkout.gateway.handleRadioChange);
                $('#id_username').focus();
            },
            handleRadioChange: function() {
                o.checkout.gateway.handleRadioSelection($(this).val());
            },
            handleRadioSelection: function(value) {
                var pwInput = $('#id_password');
                if (value == 'anonymous' || value =='new') {
                    pwInput.attr('disabled', 'disabled');
                } else {
                    pwInput.removeAttr('disabled');
                }
            }
        }
    };

    o.datetimepickers = {
        init: function() {
            o.datetimepickers.initDatePickers(window.document);
        },
        options: {
            'languageCode': 'en',
            'dateFormat': 'DD/MM/YYYY',
            'timeFormat': 'HH:mm',
            'datetimeFormat': 'DD/MM/YYYY HH:mm',
            'stepMinute': 15,
            'datetimePickerConfig': {
                icons: {
                    time: 'fas fa-clock',
                    date: 'fas fa-calendar',
                    up: 'fas fa-arrow-up',
                    down: 'fas fa-arrow-down',
                    previous: 'fas fa-chevron-left',
                    next: 'fas fa-chevron-right',
                    today: 'fas fa-calendar-check-o',
                    clear: 'fas fa-trash',
                    close: 'fas fa-times'
                }
            },
        },
        initDatePickers: function(el) {
            if ($.fn.datetimepicker) {
                $.fn.datetimepicker.Constructor.Default = $.extend(
                    {}, $.fn.datetimepicker.Constructor.Default, o.datetimepickers.options.datetimePickerConfig
                );

                var defaultDatepickerConfig = {
                    'format': o.datetimepickers.options.dateFormat,
                };
                var $dates = $(el).find('[data-oscarWidget="date"]').not('.no-widget-init').not('.no-widget-init *');
                $dates.each(function(ind, ele) {
                    var $ele = $(ele),
                        config = $.extend({}, defaultDatepickerConfig, {
                            'format': $ele.data('dateformat')
                        });
                    $ele.datetimepicker(config);
                });

                var defaultDatetimepickerConfig = {
                    'format': o.datetimepickers.options.datetimeFormat,
                    'stepping': o.datetimepickers.options.stepMinute,
                };
                var $datetimes = $(el).find('[data-oscarWidget="datetime"]').not('.no-widget-init').not('.no-widget-init *');
                $datetimes.each(function(ind, ele) {
                    var $ele = $(ele),
                        config = $.extend({}, defaultDatetimepickerConfig, {
                            'format': $ele.data('datetimeformat'),
                            'stepping': $ele.data('stepminute')
                        });
                    $ele.datetimepicker(config);
                });

                var defaultTimepickerConfig = {
                    'format': o.datetimepickers.options.timeFormat,
                    'stepping': o.datetimepickers.options.stepMinute,
                    'viewMode': 'times'
                };
                var $times = $(el).find('[data-oscarWidget="time"]').not('.no-widget-init').not('.no-widget-init *');
                $times.each(function(ind, ele) {
                    var $ele = $(ele),
                        config = $.extend({}, defaultTimepickerConfig, {
                            'format': $ele.data('timeformat'),
                            'stepping': $ele.data('stepminute'),
                        });
                    $ele.datetimepicker(config);
                });
            }
        }
    };


    o.init = function() {
        o.forms.init();
        o.datetimepickers.init();
    };

    return o;

})(oscar || {}, jQuery);
