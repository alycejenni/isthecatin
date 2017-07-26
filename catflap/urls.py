from django.conf.urls import include, url
from .settings import STATIC_ROOT
from django.views.static import serve
from catflapsite import views as siteviews, feeds as sitefeeds, forms as siteforms, admin as siteadmin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', include(siteadmin), name="admin"),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': STATIC_ROOT
    }),
    url(r"^$", siteviews.current, name="current"),
    url(r"^history$", siteviews.history, name="history"),
    url(r"^highlights$", siteviews.highlights, name="highlights"),
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
