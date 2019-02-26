$(document).ready(function(){
	$('.delete-bookmark').click(function(e){
		e.preventDefault();
		console.log('delete clicked');
		$('.modal').show();
	});
});