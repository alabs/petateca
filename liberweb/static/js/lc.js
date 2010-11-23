$(function () {
	$('#dock').Fisheye({
		maxWidth: 60,
		items: 'a',
		itemsText: 'span',
		container: '.dock-container',
		itemWidth: 100,
		proximity: 60,
		alignment : 'left',
		valign: 'bottom',
		halign : 'center'
	});
});
