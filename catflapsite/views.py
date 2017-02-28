from django.shortcuts import render, redirect
import catflapsite.utils as kitty
import catflap.settings as settings


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
    tags = kitty.load_tags()
    if tags is not None:
        keys = [k for k in keys if k.filename not in tags]
    keys = [k for k in keys if "not%20a%20cat" not in k.url]
    return render(request, "history.html", {
        "imgs": keys
    })


def notcat(request, img):
    if request.method == "POST":
        kitty.set_not_cat(img)
        return redirect(history)
