// This script helps with transliteration - Hebrew can be typed even if there is no Hebrew layout available

str = 'aשbנcבdגeקfכgעhיiןjחkלlךmצnמoםpפq/rרsדtאuוvהw\'xסyטzז,ת.ץ/.;ף\','; // Preparing character transliteration
dict = {};
str.split('').reduce(function(a,b,i,arr){	// Some magic - reducing the above string to key-value pairs.
	if(i%2) dict[a] = b;
	return b;
});	// After this, dict = {a:'ש', b:'נ', ...}
function translateChar(char){ return char in dict ? dict[char] : char; }	// Translating known keys to hebrew.
	
defer(function(){ // Waiting for jQuery

	$("[data-keyboard=he]").keypress(function(evt) { // Overriding default key press to transliterate English key strokes to hebrew letters
		if (evt.which && !evt.ctrlKey) {	// Will try to translate if there is a key press and no CTRL pressed.
			var charStr = String.fromCharCode(evt.which);
			var transformedChar = translateChar(charStr);
			if (transformedChar != charStr) {	// If transliteration is indeed needed - paste the char and don't do the default keypress behavior
				$(this).paste(transformedChar);
				return false;
			}
		}
	});

	$.prototype.paste = function(text){	// Defining a function that will paste into text areas, respecting selection
		return this.each(function(){
			with(this){
				newCursorPos = selectionStart + text.length;	// This will be the new caret position
				value = value.substring(0, selectionStart) + text + value.substring(selectionEnd);
				selectionStart = selectionEnd = newCursorPos;	// Restoring caret position
			}
		});
	};

});
