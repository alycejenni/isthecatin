from django import template
import django.urls
import re

register = template.Library()


@register.simple_tag(takes_context = True)
def isactive(context, viewname):
    if viewname == "current" and context["request"].path == "/":
        return "activepage"
    try:
        pattern = "^" + django.urls.reverse(viewname)
    except:
        pattern = viewname
    if re.search(pattern, context["request"].path):
        return "activepage"
    else:
        return "inactivepage"
