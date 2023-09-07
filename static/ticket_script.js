var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};

ready(() => {
	let click = $('#fields').val();
	$("#add_field").click(function(){
		click++;
		if (click > 5) {
            $("#add_field"). attr("disabled", true)
		} else {
		$(`<div class="form__fieldset field${click}">
		        <details>
		            <summary><span class="details">Вопрос ${click}:</span></summary>
		        </details>
		        <div class="content">
                    <div class="form__fieldset">
                        <label for="field${click}" class="form__label">Вопрос:</label>
                        <input class="form__input field${click}" id="field${click}_q" name="field${click}_q"/>
                    </div>
                    <div class="form__fieldset">
                        <label for="field${click}_ph" class="form__label">Placeholder:</label>
                        <input class="form__input field${click}" id="field${click}_ph" name="field${click}_ph"/>
                    </div>
                    <div class="form__fieldset">
                        <label for="field${click}_t" class="form__label">Тип:</label>
                        <select name="field${click}_t" id="field${click}_t" class="form__input form__select">
                            <option selected="selected" class="option" value="short">Короткий</option>
                            <option class="option" value="long">Длинный</option>
                        </select>
                    </div>
                    <div class="form__fieldset">
                        <label for="field${click}_ml" class="form__label">Максимальная длинна:</label>
                        <input type="number" class="form__input field${click}" id="field${click}_ml" name="field${click}_ml"/>
                    </div>
                    <div class="form__fieldset">
                        <label for="field${click}_r" class="form__label">Обязательно? :</label>
                        <input type="checkbox" class="form__input field${click}" id="field${click}_r" name="field${click}_r"/>
                    </div>
                </div>
            </div>`).insertBefore('#add_field');
            $('#fields').val(click)
		}
	});
    $('#reset').click(function(){
        $('#field1_q').val('');
        $('#field1_ph').val('');
        $('#field1_t').val('short');
        $('#field1_ml').val('');
        $('#field1_r').attr('checked', false);
        $('#field2_q').val('');
        $('#field2_ph').val('');
        $('#field2_t').val('short');
        $('#field2_ml').val('');
        $('#field2_r').attr('checked', false);
        $('#field3_q').val('');
        $('#field3_ph').val('');
        $('#field3_t').val('short');
        $('#field3_ml').val('');
        $('#field3_r').attr('checked', false);
        $('#field4_q').val('');
        $('#field4_ph').val('');
        $('#field4_t').val('short');
        $('#field4_ml').val('');
        $('#field4_r').attr('checked', false);
        $('#field5_q').val('');
        $('#field5_ph').val('');
        $('#field5_t').val('short');
        $('#field5_ml').val('');
        $('#field5_r').attr('checked', false);
        $('#form_title').val('');
        $('#name_field').val('0');
        $('#ticket_message_title').val('');
        $('#ticket_message_desc').val('');
        $('#ticket_footer').val('');
    });
});