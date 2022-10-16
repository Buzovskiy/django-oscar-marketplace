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