$(document).ready(function(){
	// this is confusing ... delete bookmark is located bookmarks html where this file is being imported

	$('.close-modal').click(function(){
		console.log('modal close');
		$('.modal').hide();
	});
	$('.ok-modal').click(function(){
		alert($('.ok-modal').attr('id'));
		let bookmark_id = $('.ok-modal').attr('id');
		if ($('.ok-modal').hasClass('modal-bookmark')){
			console.log("clicked on modal-bookmark");
			$.post('/bookmarks', {'bookmark_id' : bookmark_id}).done(function(){
				console.log();
			});
		}	
	});
	$('.cancel-modal').click(function(){
		$('.modal').hide();
	});
});