$(
    function setup() {
        refreshCaught();
        refreshAdditional();
        refreshGuilty();
        checkDOA();
    }
);

function refreshCaught() {
    var urlBox = $('#id_url');
    var img = $('#id_caughtintheact');
    var url = urlBox.val();
    img.attr("src", url);
}

function refreshAdditional() {
    var urlBox = $('#id_additional_image');
    var img = $('#id_additional');
    var url = urlBox.val();
    img.attr("src", url);
}

function refreshGuilty() {
    var urlBox = $('#id_guilty_cat');
    var img = $('#id_guilty');
    var url = urlBox.val();
    img.attr("src", url);
}

function checkDOA() {
    var doa = $('#id_doa');
    var kd = $('#known_deceased');
    var wasdoa = doa.is(":checked");
    if (!wasdoa) {
        kd.attr("style", "visibility: visible;")
    }
    else {
        $('#id_known_deceased').prop("checked", true);
        kd.attr("style", "visibility: hidden;");
    }
}