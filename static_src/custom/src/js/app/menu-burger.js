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