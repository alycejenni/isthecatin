from django.conf.urls import url
from catflapsite import ajax

urlpatterns = [
    url(r"^getcasualty$", ajax.ajax_get_casualty, name = "getcasualty"),
    ]
