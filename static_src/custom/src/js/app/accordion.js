$(".accordion__title").on("click", function () {
	$(this).toggleClass("active").next(".accordion__body").slideToggle();
})