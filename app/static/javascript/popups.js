var loadZoom = function () {
    $('#zoomcat').dialog({
        autoOpen: false,
        width: 'auto',
        height: 'auto',
        resizable: false,
        title: 'Look a cat',
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
        title: 'Nominate for the Hall of Infamy!',
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
        var mediaDiv = $(this).parentsUntil('.img-box').siblings('.zoomthumb').children('div');
        $(mediaDiv.html()).appendTo('#popupHighlight-media');
        var popup = $('#popupHighlight');
        var popupimg = popup.find('.media-item');
        var hdn = popup.find('.hidden-url');
        var src;
        var mediaItem = mediaDiv.children('img,video');
        if (mediaItem.prop('tagName') === 'IMG'){
            src = mediaItem.attr('src')
        }
        else if (mediaItem.prop('tagName') === 'VIDEO'){
            src = mediaItem.children('source').attr('src');
        }
        hdn.val(src);
        popupimg.removeClass('img-thumbnail');
        popupimg.addClass('img-responsive');
        popup.dialog('open');
    });
};