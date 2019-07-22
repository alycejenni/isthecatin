from django.conf.urls import url
from django.contrib import admin as djangoadmin
from django.contrib.auth.views import login, logout
from django.views.static import serve

import app.views
from app.obj import forms as siteforms
from app.pages import feeds as sitefeeds
from .settings.base import STATIC_ROOT

views = [app.views.HomeView,
         app.views.HistoryView,
         app.views.HighlightsView, app.views.HighlightsCreateView,
         app.views.CasualtiesView, app.views.CasualtiesCreateView, app.views.CasualtiesGetView,
         app.views.AdminView, app.views.AdminBulkEditView,
         app.views.SetNotCat]

urlpatterns = [url(v.url_pattern, v.as_view(), v.name) for v in views]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': STATIC_ROOT
        }),
    url(r'^catfood$', sitefeeds.CatFood(), name='catfood'),
    url(r'^login$', login, {
        'template_name': 'user/login.html',
        'authentication_form': siteforms.UserLogin
        }, name='user.login'),
    url(r'^logout/$', logout, name='user.logout'),
    url(app.views.admin.prefix + r'/tools/', djangoadmin.site.urls, name='admin.tools'),
    ]
