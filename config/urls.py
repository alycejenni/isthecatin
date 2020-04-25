from django.contrib import admin as djangoadmin
from django.contrib.auth import login, logout
from django.urls import include, path
from django.views.static import serve

from app.obj import forms as siteforms
from app.pages import feeds as sitefeeds
from .settings.base import STATIC_ROOT

urlpatterns = [
    path('', include('app.views.home', namespace='home')),
    path('admin/', include('app.views.admin.urls', namespace='catmin')),
    path('history/', include('app.views.history.urls', namespace='history')),
    path('highlights/', include('app.views.highlights.urls', namespace='highlights')),
    path('casualties/', include('app.views.casualties.urls', namespace='casualties')),
    path(r'static/<path:path>', serve, {
        'document_root': STATIC_ROOT
        }),
    path(r'catfood', sitefeeds.CatFood(), name='catfood'),
    path(r'login', login, {
        'template_name': 'user/login.html',
        'authentication_form': siteforms.UserLogin
        }, name='user.login'),
    path(r'logout', logout, name='user.logout'),
    path('admin/tools/', djangoadmin.site.urls, name='admin.tools'),
    path('set/', include('app.views.set.urls', namespace='set'))
    ]
