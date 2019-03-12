$(document).ready(function(){
	$('.show-navbar').click(function(){
		$('.mobile-sidebar').toggle(300);
	});
	document.getElementsByTagName('body')[0].onresize = function (){
		console.log("resized");
		if (window.matchMedia("(max-width: 1024px)").matches){
			$('.hamburger').show();
			$('.nav-list').hide();
		}
		else{
			$('.nav-list').show();
			$('.mobile-sidebar').hide();
			$('.hamburger').hide();
		}
	};

});