// SIDENAV
$(document).ready(function(){
	$('.show-sidebar').click(function(){
		$('.sidebar').show();
		$('.sidebar-close').show();
	});

	$('.close-sidebar').click(function(){
		$('.sidebar').hide();
	});

	// when user closes the sidebar in the mobile view, but
	// resizes to full width, then show the sidebar
	document.getElementsByTagName('body')[0].onresize = function (){
		console.log("resized");
		if (window.matchMedia("(max-width: 800px)").matches){
			console.log("less than 800px");
			$('.sidebar').hide();
		}
		else{
			console.log("greater than 800px");
			$('.sidebar').show();
		}
	};
	// adds active class to the current link 
    $('a').each(function(){
        if ($(this).prop('href') == window.location.href) {
            $(this).addClass('active'); $(this).parents('li').addClass('active');
        }
    });
})
