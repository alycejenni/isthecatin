from django import template
import django.urls
import re
import time
import os
from catflap import settings as settings

register = template.Library()


@register.simple_tag(takes_context=True)
def isactive(context, viewname):
    requestpath = context["request"].path
    try:
        url = "^" + django.urls.reverse(viewname) + "$"
    except django.urls.NoReverseMatch:
        url = viewname
    if re.search(url, requestpath):
        return "activepage"
    else:
        return "inactivepage"


@register.simple_tag
def last_committed():
    git_root = os.path.join(settings.BASE_DIR, ".git")
    try:
        modtime = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(git_root)))
    except:
        modtime = "0"
    return modtime
