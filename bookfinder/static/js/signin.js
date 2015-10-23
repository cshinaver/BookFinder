function open_sign_in() {
	$('#sign-in-dialog').modal('show');
}

function close_sign_in() {
	$('#sign-in-dialog').modal('hide');
}

function sign_in() {
	var name = document.getElementById("sign-in-field_name").value;
	document.getElementById("sign-in-name").innerHTML=name;
	
	
	document.getElementById("sign-in-button").style.display="none";
	document.getElementById("sign-in-drop-down").style.display="block";
	close_sign_in();
}

function sign_out() {
	document.getElementById("sign-in-button").style.display="block";
	document.getElementById("sign-in-drop-down").style.display="none";
}