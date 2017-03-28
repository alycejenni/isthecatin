from django.conf.urls import url
from django.contrib import admin
from .settings import STATIC_ROOT
from django.views.static import serve
from catflapsite import views as site
from catflapsite import feeds

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r"^$", site.current, name="current"),
    url(r"^history$", site.history, name="history"),
    url(r'^notcat/(?P<img>.*)$', site.notcat, name="notcat"),
    url(r'^catfood$', feeds.CatFood(), name = "catfood"),
    url(r'^rip$', site.casualties, name = "rip"),
    url(r'^ffsganja/(?P<img>.*)$', site.createcasualty, name = "ffsganja"),
]