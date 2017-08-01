from django.conf.urls import url
from catflapsite.views import admin as siteadmin, bulk_edit
from django.contrib import admin as djangoadmin

urlpatterns = [
    url(r"^$", siteadmin, name = "admin"),
    url(r"^bulkedit/(?P<page>[0-9]+)$", bulk_edit, name = "bulkedit"),
    url(r'^tools/', djangoadmin.site.urls),
    ]
