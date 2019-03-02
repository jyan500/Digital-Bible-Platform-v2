$(document).ready(function(){
	let onPageLoadBook = $("#booklist").find("option:selected").attr
	let currChapter = $("#chapterlist").find("option:selected").attr("value");


	//Populate the dropdown so user can select the chapter for the chosen book
	$("#booklist").change(function(){
		let currBook = $("#booklist").find("option:selected").attr("value");	
		console.log("currBook: " + currBook)
		if (currBook != ""){
			// delete all previous option nodes for the chapter
			$("#chapterlist").empty();
			// populate the drop down for chapters

			$.ajax({
				url: "/",
				data:  {
					'selectedbook': currBook 
				},
				type: "GET",
				dataType: "json",
				success: function (response){
					// dynamically populate the option nodes within the chapter select bar  
					console.log(response['chapterlist']);
					for (var i = 0; i < response['chapterlist'].length; i++){
						let chapter = response['chapterlist'][i]
						let newOptionNode = $("<option>").text(chapter);	
						newOptionNode.attr("value", chapter);
						$("#chapterlist").append(newOptionNode);	
					}
				},
				error: function(error){
					alert("There was a problem getting the chapters");
				}

			})
			
		}
	})



	// configure the popover
	// [data-toggle="popover"]
	$('[id*="popover"]').popover({
		html : true,
		content : function(){
			// var $verseID = this.getAttribute('data-verse');
			let verse = this.getAttribute('data-verse');
			let chapter = this.getAttribute('data-chapter');
			let book = this.getAttribute('data-book');	
	    	// $("#verse-id-" + $verseID).val("" + $verseID);
		    // show the note from the DB
		    $.ajax({
		    	url: '/note_show',
		    	dataType: 'json',
		    	data: {
		    		// 'verse-id': $verseID,	
		    		'verse' : verse,
		    		'chapter' : chapter,
		    		'book' : book
		    	},
		    	type : "GET",
		    	success: function(response){
		    		if (response){
		    			console.log(response['note_content']);
		    			$("#existing_notes_" + verse).text(response['note_content']);
		    		}
		    	},
		    	error : function(error){
		    		console.log("There was an error in showing the note");
		    	}


		    });
			return $('#popover_content_' + verse).html();
		}
		}).on('shown.bs.popover', function(e) {
		    //get the actual shown popover

		    var $popover = $(this).data('bs.popover').tip();
		   	var $hasText = false;	
		   	var $verse = this.getAttribute('data-verse'); 
	   		let $chapter = this.getAttribute('data-chapter');
			let $book = this.getAttribute('data-book');	
		   	console.log("verse here within shown.bs.popover: " + $verse);
		    $popover.find('.edit').click(function(){
		    	// existing notes should show in the text area upon clicking edit
		    	console.log("verseID within edit: " + $verse);
		    	var notes = $("#existing_notes_" + $verse).text();
		    	$("#note_section_" + $verse).val(notes);
		    	$("#existing_notes_section_" + $verse).hide();
		    	$("#form_section_" + $verse).show();
		    	$("#note_section_" + $verse).show();

	    	});
	    	console.log('existing notes: ' + $('#existing_notes').text());
	    	$popover.find('.save').click(function(e){
	    		e.preventDefault();	
	    		// check to make sure user doesn't save an empty note
		    	console.log('existing notes in save: ' + $('#existing_notes').text());
		    	var $existingNotes = $('#existing_notes_' + $verse).text();

		    	var $noteContent = $("#note_section_" + $verse).val();
	    		if ($noteContent == ""){
					$("#errorbar").addClass("show");
					setTimeout(function(){
						$("#errorbar").removeClass("show");	

					}, 3000);
					return;
				}

				$path = "";

				if ($existingNotes != ""){
					// we need to update instead of insert 
					$path = '/note_update';
				}
				else{
					$path = '/note_insert';
				}

				

	    		$.ajax({
					url: $path,
					data: {
						'verse': $verse,
						'book': $book,
						'chapter': $chapter,
						'note-content': $noteContent			
					},
					type: 'POST',
					success: function(response){
						$("#successbar").addClass("show");
						setTimeout(function(){
							$("#successbar").removeClass("show");
						}, 3000);
					},
					error: function(error){
						console.log('error in inserting');
					}
				});
	    	});
            $popover.find('.cancel').click(function(){
                //console.log('OK triggered');
                $popover.popover('hide');
	            console.log('hidden');
            });
	}); 

	// workaround for bootstrap glitch where the inState.click variable
	// is not reset when popover('hide') is called
	// code by Github user julesongithub 
	$('body').on('hidden.bs.popover', function (e) {
	    $(e.target).data("bs.popover").inState.click = false;
	});


	
});



