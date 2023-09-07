var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};

window.window.data_embed = {
    "content": "",
    "embeds": [
        {
            "title": "",
            "description": "",
            "color": 0,
            "image": {
                "url": ""
            },
            "author": {
                "name": "",
                "icon_url": ""
            },
            "footer": {
                "text": "",
            },
            "fields": [
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                },
                {
                    "name": "",
                    "value": "",
                    "inline": false
                }
            ]
        }

    ]
}
ready(() => {

    window.data_embed["embeds"][0]["author"]["name"] = $("#user_name").val();
    window.data_embed["embeds"][0]["author"]["icon_url"] = $("#user_avatar").val();
    console.log(window.data_embed)
    var bot_name = $("#bot_name").val();
    var bot_avatar = $("#bot_avatar").val();
    function utf8_to_b64( str ) {
        return encodeURIComponent(window.btoa(encodeURIComponent( str )));
    }

    $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
    $("#title").change(function(){
        window.data_embed["embeds"][0]["title"] = $("#title").val();
        let encoded = utf8_to_b64(JSON.stringify(window.data_embed));
        $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
    });


    const hexToDecimal = hex => parseInt(hex, 16);
    $("input").change(function(){
        window.data_embed["embeds"][0]["color"] = hexToDecimal(($("#color").val()).substring(1))
        const dt = new Date(new Date().toLocaleString("en-US", {timeZone: 'Europe/Moscow',}));
        const padL = (nr, len = 2, chr = `0`) => `${nr}`.padStart(2, chr);
        time = `${
            dt.getFullYear()}-${
            padL(dt.getMonth()+1)}-${
            padL(dt.getDate())} ${
            padL(dt.getHours())}:${
            padL(dt.getMinutes())}:${
            padL(dt.getSeconds())}`
        if ($("#date").is(':checked')){
            window.data_embed["embeds"][0]["footer"]["text"] = "МСК: " + time;
        }
        else {
            window.data_embed["embeds"][0]["footer"]["text"] = '';
        }
        $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
    })
    $("select").on("change", function(){
        if($("#role :selected").val() != 'no-ping'){
            window.data_embed["content"] = '<@&' + $("#role :selected").val() + '>';
            $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
        }
        else {
            window.data_embed["content"] = '';
            $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
        }
    })
    $(document).on("change", "textarea", function(){
        window.data_embed["embeds"][0]["title"] = $("#title").val();
        window.data_embed["embeds"][0]["description"] = $("#desc").val();
        window.data_embed["embeds"][0]["fields"][0]["name"] = $("#title1").val();
        console.log($("#title1").val())
        window.data_embed["embeds"][0]["fields"][0]["value"] = $("#desc1").val();
        window.data_embed["embeds"][0]["fields"][1]["name"] = $("#title2").val();
        window.data_embed["embeds"][0]["fields"][1]["value"] = $("#desc2").val();
        window.data_embed["embeds"][0]["fields"][2]["name"] = $("#title3").val();
        window.data_embed["embeds"][0]["fields"][2]["value"] = $("#desc3").val();
        window.data_embed["embeds"][0]["fields"][3]["name"] = $("#title4").val();
        window.data_embed["embeds"][0]["fields"][3]["value"] = $("#desc4").val();
        window.data_embed["embeds"][0]["fields"][4]["name"] = $("#title5").val();
        window.data_embed["embeds"][0]["fields"][4]["value"] = $("#desc5").val();
        window.data_embed["embeds"][0]["fields"][5]["name"] = $("#title6").val();
        window.data_embed["embeds"][0]["fields"][5]["value"] = $("#desc6").val();
        window.data_embed["embeds"][0]["fields"][6]["name"] = $("#title7").val();
        window.data_embed["embeds"][0]["fields"][6]["value"] = $("#desc7").val();
        window.data_embed["embeds"][0]["fields"][7]["name"] = $("#title8").val();
        window.data_embed["embeds"][0]["fields"][7]["value"] = $("#desc8").val();
        window.data_embed["embeds"][0]["fields"][8]["name"] = $("#title9").val();
        window.data_embed["embeds"][0]["fields"][8]["value"] = $("#desc9").val();
        window.data_embed["embeds"][0]["fields"][9]["name"] = $("#title10").val();
        window.data_embed["embeds"][0]["fields"][9]["value"] = $("#desc10").val();
        $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
    })




    const input = document.getElementById("pic");
    const convertBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader();
            fileReader.readAsDataURL(file);

            fileReader.onload = () => {
                resolve(fileReader.result);
            };

            fileReader.onerror = (error) => {
                reject(error);
                };
            });
        };

    const uploadImage = async (event) => {
        const file = event.target.files[0];
        const base64 = await convertBase64(file);
        window.data_embed["embeds"][0]["image"]["url"] = base64;
        $(".iframe").attr("src", "/static/embed_builder/embed_builder.html?username=" + encodeURIComponent(bot_name) + "&avatar=" + encodeURIComponent(bot_avatar));
    };

    input.addEventListener("change", (e) => {
        uploadImage(e);
    });
});