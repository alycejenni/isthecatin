from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.views.static import serve

from catflapsite.obj import forms as siteforms
from catflapsite.pages import feeds as sitefeeds, views as siteviews
from catflapsite.urls import admin as siteadmin, ajax as siteajax
from .settings import STATIC_ROOT

urlpatterns = [
    url(r'^admin/', include(siteadmin), name="admin"),
    url(r'^ajax/', include(siteajax), name = "ajax"),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': STATIC_ROOT
    }),
    url(r"^$", siteviews.current, name="current"),
    url(r"^history/(?P<page>[0-9]+)$", siteviews.history, name="history"),
    url(r"^highlights/(?P<page>[0-9]+)$", siteviews.highlights, name="highlights"),
    url(r'^notcat/(?P<img>.*)$', siteviews.notcat, name="notcat"),
    url(r'^catfood$', sitefeeds.CatFood(), name="catfood"),
    url(r'^rip$', siteviews.casualties, name="rip"),
    url(r'^ffsganja/(?P<img>.*)$', siteviews.createcasualty, name="ffsganja"),
    url(r'^submitcasualty$', siteviews.submitcasualty, name="submitcasualty"),
    url(r"^nominate$", siteviews.nominate, name="nominate"),
    url(r'^login$', login, {
        'template_name': 'user/login.html',
        'authentication_form': siteforms.UserLogin
    }, name='login'),
    url(r'^logout/$', logout, name='logout'),
]
