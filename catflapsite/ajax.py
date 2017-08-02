from .models import Casualty
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
import ast
from .utils import conn as kitty


def ajax_get_casualty(request):
    if request.method == "GET":
        pk = int(request.GET.get("pk", None))
        casualty_obj = Casualty.objects.get(pk = pk)
        casualty_json = serializers.serialize("json", [casualty_obj])
        casualty_dict = ast.literal_eval(
            casualty_json[1:-1].split("\"fields\": ")[1][0:-1].replace("false", "False").replace("true", "True"))
        catflap = render_to_string("../templates/fragments/media.html", {
            "src": kitty.get_cat_from_url(casualty_dict["url"])
        })
        casualty_dict["catflap_media"] = catflap
        if casualty_dict["additional_image"] != "":
            critter = render_to_string("../templates/fragments/media.html", {
                "src": kitty.get_cat_from_url(casualty_dict["additional_image"])
            })
            casualty_dict["critter_media"] = critter
        if casualty_dict["guilty_cat"] != "":
            guilty = render_to_string("../templates/fragments/media.html", {
                "src": kitty.get_cat_from_url(casualty_dict["guilty_cat"])
            })
            casualty_dict["guilty_media"] = guilty
        return JsonResponse(casualty_dict)
    else:
        return JsonResponse({})
