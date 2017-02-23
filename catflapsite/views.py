from django.shortcuts import render
from datetime import datetime as dt
import pytz
import boto
import catflap.settings as settings


def mainpage(request):
    london = pytz.timezone("Europe/London")
    s3 = boto.connect_s3(settings.AWS_KEY, settings.AWS_SECRET, host = "s3.eu-west-2.amazonaws.com")
    bucket = s3.get_bucket(settings.IMAGE_BUCKET)
    key = next((k for k in bucket.get_all_keys() if k.is_latest))
    if key is not None:
        imgurl = key.generate_url(expires_in = 0, query_auth = False)
        timeago = london.localize(dt.now()) - key.last_modified
        return render(request, "main.html", {"imgurl": imgurl, "timeago": timeago})
    else:
        imgurl = None
        timeago = london.localize(dt.now())