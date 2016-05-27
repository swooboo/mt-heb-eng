defer(function(){ // Waiting for jQuery
	$("#source").focus();	// Focus on the source input
	
	$("input#go").click(function(){	// Button sends AJAX to retrieve translation
		req = {};
		req.sentence = $("textarea#source").val();
		$.ajax({
			url: "/tr",
			type: "POST",
			data: req,
			success: function(resp){ $("textarea#target").val(resp.sentence); },
			error: function(){ console.log("AJAX to '/tr' with sentence '" + req.sentence + "' failed."); }
		});
	});

	$("form#tr").submit(function(){	// Don't submit form
		return false;
	});

	$('#source').keydown(function (e){
		if (e.ctrlKey && e.keyCode == 13)	// Submitting on CTRL+Enter
			 $("input#go").click();
	});
});


function defer(method) { // Function that waits for jQuery, then executes method
	if (window.jQuery)
		method();
	else
		setTimeout(function() { defer(method) }, 50);
}
