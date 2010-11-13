$(function () {
	$('#dock').Fisheye({
		maxWidth: 30,
		items: 'a',
		itemsText: 'span',
		container: '.dock-container',
		itemWidth: 50,
		proximity: 60,
		alignment : 'left',
		valign: 'bottom',
		halign : 'center'
	});
});
