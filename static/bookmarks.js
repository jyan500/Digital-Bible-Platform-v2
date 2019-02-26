$(document).ready(function(){
	$('.delete-bookmark').click(function(e){
		e.preventDefault();
		console.log('delete clicked');
		let id = $(this).attr('id');
		console.log(id);
		$('.modal').show();
		$('.ok-modal').attr('id', id);
		$('.ok-modal').addClass('modal-bookmark');
		console.log('ok-modals id: ' , $('.ok-modal').attr('id'));
		console.log('ok-modals class: ' , $('.ok-modal').attr('class'));
	});
});