from django.conf.urls import url
from django.contrib import admin as djangoadmin

from app.pages import views

urlpatterns = [
    url(r"^$", views.admin, name = "admin"),
    url(r"^bulkedit/(?P<page>[0-9]+)$", views.bulk_edit, name = "bulkedit"),
    url(r'^tools/', djangoadmin.site.urls),
    ]
