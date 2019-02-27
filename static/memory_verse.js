$(document).ready(function(){
	// set the height of the front to be the same as the back of card
	$(".front").click(function(){
		if ($(".verse-number").css('visibility') == 'hidden' && $(".individual-verse").css('visibility') == 'hidden'){
			$(".verse-number").css('visibility', 'visible');
			$(".verse-number").css('opacity', 1);
			$(".individual-verse").css('visibility', 'visible');
			$(".individual-verse").css('opacity', 1);
		}
		else{
			$(".verse-number").css('visibility', 'hidden');
			$(".individual-verse").css('visibility', 'hidden');
			$(".verse-number").css('opacity', 0);
			$(".individual-verse").css('opacity', 0);
		}
	});
	// when user clicks on span, get the id of the span
	$(".delete-verse").click(function(e){
		e.preventDefault();
		let id = $(this).attr('id');
		$('.modal').show();
		$('.id-to-submit').val(id);
		$('.id-to-submit').addClass('modal-memory-verse');
	});

});
