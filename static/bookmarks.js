$(document).ready(function(){
	$('.delete-bookmark').click(function(e){
		e.preventDefault();
		console.log('delete clicked');
		let id = $(this).attr('id');
		console.log(id);

		// these classes are coming from modal.html
		$('.modal').show();
		$('.id-to-submit').val(id);
		$('.id-to-submit').addClass('modal-bookmark');
		console.log('ok-modals id: ' , $('.id-to-submit').val());
		console.log('id to submit class: ' , $('.id-to-submit').attr('class'));
	});
});