from django.shortcuts import render, redirect
import catflapsite.utils as kitty
import os.path
import pickle
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
        keys = [k for k in keys if k.id not in tags or tags[k.id]]
    else:
        with open(settings.IMG_PKL, "wb") as file:
            pickle.dump({ k.id: True for k in keys }, file)
    splitbysix = [keys[i:i + 6] for i in range(0, len(keys), 6)]
    return render(request, "history.html", {
        "imgrows": splitbysix
    })


def notcat(request, img):
    if request.method == "POST":
        kitty.set_tag(img, False)
        return redirect(history)
