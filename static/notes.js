$(document).ready(function(){
	// when user clicks on span, get the id of the span
	$(".delete-verse").click(function(e){
		e.preventDefault();
		// transfer the id of the span to the id within modal for submit
		let id = $(this).attr('id');
		$('.modal').css('z-index', 2)
		$('.modal').show();
		$('.id-to-submit').val(id);
		$('.id-to-submit').addClass('modal-notes');
	});
});