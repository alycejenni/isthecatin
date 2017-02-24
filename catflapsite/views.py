from django.shortcuts import render
from datetime import datetime as dt
import catflapsite.utils as kitty


def current(request):
    key = kitty.get_latest_s3()
    if key is not None:
        imgurl = key.generate_url(expires_in=0, query_auth=False)
        timeago = kitty.now() - kitty.localise(dt.strptime(key.last_modified, "%Y-%m-%dT%H:%M:%S.000Z"))
    else:
        imgurl = None
        timeago = kitty.now()
    return render(request, "main.html", {
        "imgurl": imgurl,
        "timeago": timeago
    })

def history(request):
    keys = [k.generate_url(expires_in=0, query_auth=False) for k in kitty.get_all_s3()]
    splitbysix = [keys[i:i + 6] for i in range(0, len(keys), 6)]
    return render(request, "history.html", {
        "imgrows": splitbysix
    })