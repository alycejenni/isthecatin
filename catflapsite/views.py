from django.shortcuts import render, redirect
import catflapsite.utils as kitty


def current(request):
    key = kitty.get_latest_s3()
    return render(request, "main.html", {
        "img": key
    })


def history(request):
    keys = kitty.get_key_objects()
    keys = [k for k in keys if k.iscat]
    return render(request, "history.html", {
        "imgs": keys
    })


def notcat(request, img):
    if request.method == "POST":
        kitty.set_not_cat(img)
        return redirect(history)
