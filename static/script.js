var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};


ready(() => {
    let click = 0;
	$("#button_add").on("click", function(){
		click++;
		if (click > 10) {
            $("#button_add").attr("disabled", true)
		} else {
		$(`<div class="form__fieldset">
			<label for="title${click}" class="form__label">Тема ${click}:</label>
			<div class="area">
			<textarea name="title${click}" id="title${click}" class="form__input"></textarea>
			</div>
		</div>
		<div class="form__fieldset">
			<label for="desc${click}" class="form__label">Описание ${click}:</label>
			<div class="area">
			<textarea name="desc${click}" id="desc${click}" class="form__input"></textarea>
			</div>
		</div>`).insertBefore('#place');
		}
	});
    
});