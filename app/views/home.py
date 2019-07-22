from django.shortcuts import render
from django.views import View


class HomeView(View):
    url_pattern = r'^$'
    name = 'home.index'

    def get(self, request):
        return render(request, 'main.html', {
            'img': kitty.latest_cat
            })
