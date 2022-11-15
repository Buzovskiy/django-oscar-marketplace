$('.bannerslide__content').slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	dots: false,
	arrows: true,
	autoplay: true,
	responsive: [{
		breakpoint: 991,
		settings: {
			dots: true,
			arrows: false,
		}
	}, ]
});