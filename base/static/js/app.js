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
		};
		
		var _get = function() {
			return document.querySelector(selector);
		};
		
		return {
			applyAll: _applyAll,
			get: _get
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
		el.addEventListener('click', function() {
			document.querySelector('#loading-bar').classList.remove("escondido");
		});
	});
	
	JQ("dialog").applyAll(function(el, index) {
		if (!el.showModal) {
			dialogPolyfill.registerDialog(el);
		}
	});
	
	JQ("[data-opendialog]").applyAll(function(el, index) {
		el.addEventListener("click", function(event) {
			JQ(event.currentTarget.getAttribute("data-opendialog")).get().showModal();
		});
	});
	
	JQ("[data-closedialog]").applyAll(function(el, index) {
		el.addEventListener("click", function(event) {
			JQ(event.currentTarget.getAttribute("data-closedialog")).get().close();
		});
	});
	
	JQ(".mdl-snackbar.mdl-snackbar--active").applyAll(function(el, index) {
		setTimeout(function() {
			el.classList.remove("mdl-snackbar--active");
		}, 2000);
	});
	
});