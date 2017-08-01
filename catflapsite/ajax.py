from .models import Casualty
from django.core import serializers
from django.http import JsonResponse
import ast


def ajax_get_casualty(request):
    if request.method == "GET":
        pk = int(request.GET.get("pk", None))
        casualty_obj = Casualty.objects.get(pk=pk)
        casualty_json = serializers.serialize("json", [casualty_obj])
        casualty_dict = ast.literal_eval(casualty_json[1:-1].split("\"fields\": ")[1][0:-1].replace("false", "False").replace("true", "True"))
        return JsonResponse(casualty_dict)
    else:
        return JsonResponse({})
