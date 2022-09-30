$(window).scroll(function () {
	let height = $(window).scrollTop();
	if (height > 350) {
		$('header').addClass('active');
	} else {
		$('header').removeClass('active');
	}
});