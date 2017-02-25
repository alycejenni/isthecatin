from django.shortcuts import render
import catflapsite.utils as kitty


def current(request):
    key = kitty.get_latest_s3()
    if key is not None:
        img = kitty.ImgUrl(key)
    else:
        img = None
    return render(request, "main.html", {
        "img": img
    })


def history(request):
    keys = [kitty.ImgUrl(k) for k in kitty.get_all_s3()]
    splitbysix = [keys[i:i + 6] for i in range(0, len(keys), 6)]
    return render(request, "history.html", {
        "imgrows": splitbysix
    })
