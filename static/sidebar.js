// SIDENAV
$(document).ready(function(){
	// // adds active class to the current link 
 //    $('a').each(function(){
 //        if ($(this).prop('href') == window.location.href) {
 //            $(this).addClass('active'); $(this).parents('li').addClass('active');
 //        }
 //    });
	$('.show-sidebar').click(function(){
		$('.mobile-sidebar').toggle(300);
	});
	// when user closes the sidebar in the mobile view, but
	// resizes to full width, then show the sidebar
	document.getElementsByTagName('body')[0].onresize = function (){
		console.log("resized");
		if (window.matchMedia("(max-width: 800px)").matches){
			// console.log("less than 800px");
			$('.mobile-sidebar').hide();
			$('.hamburger').show();
			$('.sidebar').hide();
		}
		else{
			// console.log("greater than 800px");
			$('.sidebar').show();
			$('.mobile-sidebar').hide();
			$('.hamburger').hide();
		}
	};
	
})
