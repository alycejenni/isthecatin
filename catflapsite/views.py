from django.shortcuts import render, redirect
from .utils import conn as kitty
from .utils import ImgUrl
from .forms import CreateCasualty


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


def casualties(request):
    return render(request, "rip.html")


def submitcasualty(request):
    if request.method == "POST":
        form = CreateCasualty(request.POST)
        if form.is_valid():
            form.save()


def createcasualty(request, img):
    if request.method == "POST":
        img = ImgUrl(kitty.get_key(img))
        form = CreateCasualty(request, initial = { 'url': img.url })
        return render(request, "createcasualty.html", { "form": form, "img": img })
    elif img:
        img = ImgUrl(kitty.get_key(img))
        form = CreateCasualty(initial = { 'url': img.url })
        return render(request, "createcasualty.html", { "form": form, "img": img })
    else:
        form = CreateCasualty(initial = {
            'url': "https://upload.wikimedia.org/wikipedia/commons/1/1e/Large_Siamese_cat_tosses_a_mouse.jpg" })
        return render(request, "createcasualty.html", { "form": form })
