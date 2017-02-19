from django.shortcuts import render
from .models import Image
import base64
from datetime import datetime as dt
import pytz


def mainpage(request):
    img = Image.objects.first()
    b64img = base64.b64encode(img.imgdata)
    london = pytz.timezone("Europe/London")
    timeago = london.localize(dt.now()) - img.timetaken
    return render(request, "main.html", {"imgdata": b64img, "timetaken": img.timetaken, "timeago": timeago})