// call with a url and a callback function to run after downloading.
// the first argument of the callback function is the content of the file at the specified url.
// EX:
//	get_file('test.txt', function(text) {
//		alert(text);
//	});
function get_file(strURL, callback) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			callback(xhttp.responseText);
		}
	}
	xhttp.open("GET", strURL, true);
	xhttp.send();
}
