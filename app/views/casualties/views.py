import ast

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

from app.obj.custom import ImgUrl
from app.obj.forms import CreateCasualty
from app.obj.models import Casualty
from app.utils.db import conn


class IndexView(View):
    url_pattern = ''
    name = 'index'

    def get(self, request):
        animals = conn.get_cats_from_objects(Casualty.objects, 0, None, ['known_deceased'], True)
        return render(request, 'rip.html', {
            'animals': animals
            })


class CreateView(View):
    url_pattern = 'create'
    name = 'create'

    def get(self, request):
        img = request.POST.get('img', None)
        if img is not None:
            img = ImgUrl(conn.get_key(img))
            form = CreateCasualty(initial={
                'url': img.url,
                'time_taken': img.time_taken.strftime('%Y-%m-%d')
                })
            return render(request, 'createcasualty.html', {
                'form': form,
                'img': img
                })
        else:
            form = CreateCasualty(initial={
                'url': 'https://upload.wikimedia.org/wikipedia/commons/1/1e'
                       '/Large_Siamese_cat_tosses_a_mouse.jpg'
                })
            return render(request, 'createcasualty.html', {
                'form': form
                })

    def post(self, request):
        if request.method == 'POST':
            form = CreateCasualty(request.POST)
            if form.is_valid():
                form.save()
                print('saved')
        return redirect('casualties:index')


class SingleView(View):
    url_pattern = 'view'
    name = 'single'

    def get(self, request):
        pk = int(request.GET.get('pk', None))
        casualty_obj = Casualty.objects.get(pk=pk)
        casualty_json = serializers.serialize('json', [casualty_obj])
        casualty_dict = ast.literal_eval(
            casualty_json[1:-1].split("\"fields\": ")[1][0:-1].replace("false", "False").replace(
                "true", "True"))
        catflap = render_to_string("../templates/fragments/media.html", {
            "src": conn.get_cat_from_url(casualty_dict["url"])
            })
        casualty_dict["catflap_media"] = catflap
        if casualty_dict["additional_image"] != "":
            critter = render_to_string("../templates/fragments/media.html", {
                "src": conn.get_cat_from_url(casualty_dict["additional_image"])
                })
            casualty_dict["critter_media"] = critter
        if casualty_dict["guilty_cat"] != "":
            guilty = render_to_string("../templates/fragments/media.html", {
                "src": conn.get_cat_from_url(casualty_dict["guilty_cat"])
                })
            casualty_dict["guilty_media"] = guilty
        return JsonResponse(casualty_dict)
