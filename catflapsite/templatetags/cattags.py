from django import template
import django.urls
import re

register = template.Library()


@register.simple_tag(takes_context = True)
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
