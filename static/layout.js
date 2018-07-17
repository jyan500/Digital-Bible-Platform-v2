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
	$('[data-toggle="popover"]').popover(); 

})

