from django.shortcuts import render
from django.urls import path
from django.views import View

from app.utils.db import conn


class HomeView(View):
    url_pattern = ''
    name = 'index'

    def get(self, request):
        return render(request, 'main.html', {
            'img': conn.latest_cat
            })

app_name = 'home'
urlpatterns = [path('', HomeView.as_view(), name='index')]
