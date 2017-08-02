from django.conf.urls import url
from django.contrib import admin as djangoadmin

from catflapsite.pages.views import admin as siteadmin, bulk_edit

urlpatterns = [
    url(r"^$", siteadmin, name = "admin"),
    url(r"^bulkedit/(?P<page>[0-9]+)$", bulk_edit, name = "bulkedit"),
    url(r'^tools/', djangoadmin.site.urls),
    ]
