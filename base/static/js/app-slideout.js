var slideout = new Slideout({
	'panel': document.getElementById('panel'),
	'menu': document.getElementById('menu'),
	'padding': 256,
	'tolerance': 70
});

document.querySelector("#btn-menu").addEventListener("click", function(){
	slideout.toggle(); 
});