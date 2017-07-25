var loadZoom = function () {
    $('#zoomcat').dialog({
        autoOpen: false,
        width: 'auto',
        height: 'auto',
        resizable: false,
        show: {
            effect: 'fade',
            duration: 500
        },
        hide: {
            effect: 'fade',
            duration: 500
        }
    });
    $('.zoomthumb').on('click', function () {
        $('#zoomcat-body').empty();
        $($(this).children('div').html()).appendTo('#zoomcat-body');
        var zoomcat = $('#zoomcat');
        var zoomcatimg = zoomcat.find('img');
        zoomcatimg.removeClass('img-thumbnail');
        zoomcatimg.addClass('img-responsive');
        zoomcat.dialog('open');
    });
};

var loadNominate = function () {
    $('#popupHighlight').dialog({
        autoOpen: false,
        width: 'auto',
        height: 'auto',
        resizable: false,
        show: {
            effect: 'fade',
            duration: 500
        },
        hide: {
            effect: 'fade',
            duration: 500
        }
    });
    $('.addhighlight').on('click', function () {
        $('#popupHighlight-media').empty();
        $('#popupHighlight-comment').val('');
        var mediaItem = $(this).parentsUntil('.img-box').siblings('.zoomthumb').children('div');
        $(mediaItem.html()).appendTo('#popupHighlight-media');
        var popup = $('#popupHighlight');
        var popupimg = popup.find('.media-item');
        var hdn = popup.find('.hidden-url');
        var src = mediaItem.attr('src');
        hdn.val('uhbbib');
        popupimg.removeClass('img-thumbnail');
        popupimg.addClass('img-responsive');
        popup.dialog('open');
    });
};