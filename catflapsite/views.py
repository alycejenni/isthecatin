import base64

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .utils import conn as kitty
from .utils import ImgUrl
from .forms import CreateCasualty
from .models import Casualty, Highlight
from django.core import serializers


def current(request):
    return render(request, "main.html", {
        "img": kitty.latest_cat
    })


def history(request):
    PAGE_SIZE_LIMIT = 18
    return render(request, "history.html", {
        "imgs": kitty.cats[0:PAGE_SIZE_LIMIT]
    })


def highlights(request):
    PAGE_SIZE_LIMIT = 18
    return render(request, "highlights.html", {
        "imgs": Highlight.objects.all()[0:PAGE_SIZE_LIMIT]
        })


def notcat(request, img):
    if request.method == "POST":
        try:
            kitty.set_not_cat(img)
        except Exception as e:
            print(e)
        return redirect(history)


def casualties(request):
    animal_objects = Casualty.objects.all()

    animals = []
    for a in animal_objects:
        animals.append({
            "object": a,
            "encoded": base64.b64encode((serializers.serialize('json', [a])).encode())
        })
    return render(request, "rip.html", {
        "animals": animals
    })


def submitcasualty(request):
    if request.method == "POST":
        form = CreateCasualty(request.POST)
        if form.is_valid():
            form.save()
            print("saved")
    return redirect("rip")


def createcasualty(request, img):
    if img is not None:
        img = ImgUrl(kitty.get_key(img))
        form = CreateCasualty(initial={
            'url': img.url
        })
        return render(request, "createcasualty.html", {
            "form": form,
            "img": img
        })
    else:
        form = CreateCasualty(initial={
            'url': "https://upload.wikimedia.org/wikipedia/commons/1/1e/Large_Siamese_cat_tosses_a_mouse.jpg"
        })
        return render(request, "createcasualty.html", {
            "form": form
        })


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, "admin/admin.html")


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def bulk_edit(request, page="1"):
    page_size_limit = 36
    page = int(page)
    page_start = (page - 1) * page_size_limit
    page_end = page * page_size_limit
    template = "admin/bulkedit.html"
    if request.method == "POST" and "display" in request.POST:
        items = []
        displaytype = request.POST["display"]
        if displaytype == "cats":
            items = kitty.cats
        elif displaytype == "all":
            items = kitty.custom_keys
        elif displaytype == "notcats":
            items = kitty.notcats
        return render(request, template, {
            "imgs": items[page_start:page_end],
            "displaytype": displaytype,
            "page": page
        })
    elif request.method == "POST" and "btn_submit" in request.POST:
        btn = request.POST["btn_submit"]
        if btn == "Next page":
            return redirect("bulkedit", page=str(page+1))
        elif btn == "Previous page":
            return redirect("bulkedit", page=str(page-1))
        elif btn == "No cats here":
            btn_method = kitty.set_not_cat
        elif btn == "Delete these":
            btn_method = kitty.delete_key

        if "items" in request.POST:
            items = request.POST.getlist("items")

            for i in items:
                try:
                    btn_method(i)
                except:
                    pass
            return render(request, template, {
                "imgs": kitty.cats[page_start:page_end],
                "page": page
            })
    else:
        return render(request, template, {
            "imgs": kitty.cats[page_start:page_end],
            "page": page
        })
