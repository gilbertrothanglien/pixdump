$(function() {
	'use strict';
	
  $('.form-control').on('input', function() {
	  var $field = $(this).closest('.form-group');
	  if (this.value) {
	    $field.addClass('field--not-empty');
	  } else {
	    $field.removeClass('field--not-empty');
	  }
	});

});

function register(){
	document.querySelector("#login").style.display = "none";
	document.querySelector("#register").style.display = "block";
}
function login(){
	document.querySelector("#login").style.display = "block";
	document.querySelector("#register").style.display = "none";
}