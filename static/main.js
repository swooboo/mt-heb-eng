defer(function(){ // Waiting for jQuery
	$("#source").focus();	// Focus on the source input
});

$("input#go").click(function(){
	req = {};
	req.sentence = $("textarea#source").val();
	$.ajax({
		url: "/tr",
		type: "POST",
		data: req,
		success: function(resp){ $("textarea#target").val(resp.sentence); },
		error: function(){ console.log("AJAX to '/tr' with sentence '" + req.sentence + "' failed."); }
	})
})

$("form#tr").submit(function(){
	return false;
});

function defer(method) { // Function that waits for jQuery, then executes method
	if (window.jQuery)
		method();
	else
		setTimeout(function() { defer(method) }, 50);
}
