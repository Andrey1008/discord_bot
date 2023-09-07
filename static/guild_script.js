var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};

ready(() => {
	$("textarea").each(function () {
  		this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
		}).on("input", function () {
        this.style.height = '4em';
  		this.style.height = (this.scrollHeight) + "px";
    });
    $("#button_add").on("click", function(){
		$("textarea").each(function () {
  			this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
			}).on("input", function () {
            this.style.height = '4em';
  			this.style.height = (this.scrollHeight) + "px";
		});
	});
});