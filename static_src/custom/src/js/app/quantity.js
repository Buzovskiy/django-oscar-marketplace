//Quantity
$(document).ready(function () {
	$('.quantity__button_minus').click(function () {
		let $input = $(this).parent().find('input');
		let count = parseInt($input.val()) - 1;
		count = count < 1 ? 1 : count;
		$input.val(count);
		$input.change();
		return false;
	});
	$('.quantity__button_plus').click(function () {
		let $input = $(this).parent().find('input');
		$input.val(parseInt($input.val()) + 1);
		$input.change();
		return false;
	});
});