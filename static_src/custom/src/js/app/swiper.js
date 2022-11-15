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