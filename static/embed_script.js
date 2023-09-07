var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
};

ready(() => {
    let data = {
    "content": "ХуйХуйХуйХуйХуй",
    "embeds": [
        {
            "title": "hello",
        }

    ]
}
    function utf8_to_b64( str ) {
        return encodeURIComponent(window.btoa(encodeURIComponent( str )));
    }
    $(".iframe").attr("src", "https://glitchii.github.io/embedbuilder/?nouser&embed&data=" + utf8_to_b64(JSON.stringify(data)));
    $(".title").change(function(){
        data["embeds"][0]["title"] = $(".title").val();
        let encoded = utf8_to_b64(JSON.stringify(data));
        console.log(encoded);
        $(".iframe").attr("src", "https://glitchii.github.io/embedbuilder/?nouser&embed&data=" + encoded);
        $(".object").attr("data", "https://glitchii.github.io/embedbuilder/?nouser&embed&data=" + encoded);
    });
    // convert file to a base64 url
    const readURL = file => {
        return new Promise((res, rej) => {
            const reader = new FileReader();
            reader.onload = e => res(e.target.result);
            reader.onerror = e => rej(e);
            reader.readAsDataURL(file);
        });
    };
    const fileInput = document.getElementById('pic');
    const preview = async event => {
        const file = event.target.files[0];
        const url = await readURL(file);
        console.log(url)
    };
    fileInput.addEventListener('change', preview);
});