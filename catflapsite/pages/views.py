from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from catflapsite.obj.forms import CreateCasualty, NominateHighlight
from catflapsite.obj.models import Casualty, Highlight
from catflapsite.utils import db, kitty
from catflapsite.obj.custom import ImgUrl


def current(request):
    return render(request, "main.html", {
        "img": kitty.latest_cat
    })


def history(request, page="1"):
    page = int(page)
    if request.method == "POST" and "btn_submit" in request.POST:
        btn = request.POST["btn_submit"]
        if btn == "Next page":
            return redirect("history", page=str(page + 1))
        elif btn == "Previous page":
            return redirect("history", page=str(page - 1))
    page_size_limit = 18
    page_start = (page - 1) * page_size_limit
    page_end = page * page_size_limit
    is_mod = request.user.groups.filter(name__in=['Moderators', 'Admin']).exists()
    return render(request, "history.html", {
        "imgs": kitty.cats(page_start, page_size_limit),
        "nomination_form": NominateHighlight(),
        "page": page,
        "more_pages": len(kitty.cats(page_end, 1)) != 0,
        "is_mod": is_mod or request.user.is_superuser
    })


def highlights(request, page="1"):
    page = int(page)
    if request.method == "POST" and "btn_submit" in request.POST:
        btn = request.POST["btn_submit"]
        if btn == "Next page":
            return redirect("highlights", page=str(page + 1))
        elif btn == "Previous page":
            return redirect("highlights", page=str(page - 1))
    page_size_limit = 20
    page_start = (page - 1) * page_size_limit
    page_end = page * page_size_limit
    imgs = db.get_cats_from_objects(Highlight.objects, page_start, page_end, ["comment"])
    return render(request, "highlights.html", {
        "imgs": imgs,
        "page": page,
        "more_pages": (len(imgs) != 0) and (page_end < len(imgs) - 1)
    })


def nominate(request):
    if request.method == "POST":
        form = NominateHighlight(request.POST)
        if form.is_valid():
            form.save()
            print("saved")
    return redirect("highlights", page="1")


def notcat(request, img):
    if request.method == "POST":
        try:
            kitty.set_not_cat(img)
        except Exception as e:
            print(e)
        return redirect(history, page="1")


def casualties(request):
    animals = db.get_cats_from_objects(Casualty.objects, 0, None, ["known_deceased"], True)
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
            'url': img.url,
            'time_taken': img.time_taken.strftime('%Y-%m-%d')
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
            items = kitty.cats(page_start, page_size_limit)
        elif displaytype == "all":
            items = kitty.custom_keys(page_start, page_size_limit)
        elif displaytype == "notcats":
            items = kitty.notcats(page_start, page_size_limit)
        return render(request, template, {
            "imgs": items,
            "displaytype": displaytype,
            "page": page
        })
    elif request.method == "POST" and "btn_submit" in request.POST:
        btn = request.POST["btn_submit"]
        if btn == "Next page":
            return redirect("bulkedit", page=str(page + 1))
        elif btn == "Previous page":
            return redirect("bulkedit", page=str(page - 1))
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
                "imgs": kitty.cats(page_start, page_size_limit),
                "page": page
            })
    else:
        return render(request, template, {
            "imgs": kitty.cats(page_start, page_size_limit),
            "page": page
        })
