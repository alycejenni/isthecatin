$(function refreshImage(){
    var urlBox = $('#id_url');
    var img = $('#id_caughtintheact');
    var url = urlBox.val();
    img.attr("src", url);
});