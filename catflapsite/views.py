from django.shortcuts import render, redirect
from catflapsite.utils import conn as kitty


def current(request):
    return render(request, "main.html", {
        "img": kitty.latest_cat
    })


def history(request):
    return render(request, "history.html", {
        "imgs": kitty.cats
    })


def notcat(request, img):
    if request.method == "POST":
        try:
            kitty.set_not_cat(img)
        except Exception as e:
            print(e)
        return redirect(history)
