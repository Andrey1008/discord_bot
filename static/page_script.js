var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};

ready(() => {
	let searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('page')){
      	let param = searchParams.get('page');
    	$("#page").val(param);  
    }
});