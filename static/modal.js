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
			path = '/memory_verse_post';
		}
		else if ($('.id-to-submit').hasClass('modal-notes')){
			path = '/note_delete';	
		}
		console.log("clicked on modal-bookmark");
		$('.submit-modal').attr('action', path);
		$('.submit-modal').submit();
	});
	$('.cancel-modal').click(function(e){
		e.preventDefault();
		$('.modal').hide();
	});
	$('.close-modal').click(function(e){
		e.preventDefault();
		$('.modal').hide();
	});
});