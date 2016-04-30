$("input#go").click(function(){
	req = {};
	req.sentence = $("input#source").val();
	$.ajax({
		url: "/tr",
		type: "POST",
		data: req,
		success: function(resp){ $("input#target").val(resp.sentence); },
		error: function(){ alert("AJAX to '/tr' with sentence '" + req.sentence + "' failed."); }
	})
})
