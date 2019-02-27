$(document).ready(function(){
	// this is confusing ... delete bookmark is located bookmarks html where this file is being imported
	let path = "";
	$('.close-modal').click(function(){
		console.log('modal close');
		$('.modal').hide();
	});
	$('.ok-modal').click(function(){
		if ($('.id-to-submit').hasClass('modal-bookmark')){
			path = '/bookmarks_post';
		}	
		else if ($('.id-to-submit').hasClass('modal-memory-verse')){
			path = '/memory_verse';
		}
		console.log("clicked on modal-bookmark");
		$('.submit-modal').attr('action', path);
		$('.submit-modal').submit();
	});
	$('.cancel-modal').click(function(){
		$('.modal').hide();
	});
});