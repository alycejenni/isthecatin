from django.urls import path

from . import views

view_classes = [views.IndexView, views.CreateView]

app_name = 'highlights'
urlpatterns = [path(v.url_pattern, v.as_view(), name=v.name) for v in view_classes]
