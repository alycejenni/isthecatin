from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^$", admin, name="admin"),
    url(r"^bulkedit/(?P<page>[0-9]+)$", bulk_edit, name="bulkedit")
]