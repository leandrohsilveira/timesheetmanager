//e$ = function(e) {
//	var tipo = typeof e;
//	if(tipo === "function") {
//		document.addEventListener('DOMContentLoaded', e);
//	}
//}
var JQ = function(selector) {
	if (typeof selector === "string") {
		var _applyAll = function(each) {
			var elems = document.querySelectorAll(selector);
			for(var i = 0; i < elems.length; i++) {
				each(elems[i], i);
			}
			return elems;
		}
		
		return {
			applyAll: _applyAll
		};
	} else if(typeof selector === "function") {
		document.addEventListener('DOMContentLoaded', selector);
		return document;
	} else {
		return selector;
	}
};

JQ(function() {
	
	JQ(".make-navigation").applyAll(function(el, index) {
		console.log(el);
		el.addEventListener('click', function() {
			document.querySelector('#loading-bar').classList.remove("escondido");
		});
	});
	
});