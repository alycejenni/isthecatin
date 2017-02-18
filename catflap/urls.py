from django.conf.urls import url
from django.contrib import admin
from .settings import STATIC_ROOT
from django.views.static import serve
from catflapsite import views as site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r"^$", site.mainpage),
    url(r'^/img/(?P<imgdata>.*)$', site.setimage),
]
