from django.shortcuts import render
from .models import Image
import base64
from datetime import datetime as dt


def mainpage(request):
    img = Image.objects.first()
    b64img = base64.b64encode(img.imgdata)
    timeago = dt.now() - img.timetaken.time()
    return render(request, "main.html", {"imgdata": b64img, "timetaken": img.timetaken, "timeago": timeago})
