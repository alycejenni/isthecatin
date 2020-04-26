from django.shortcuts import redirect, render
from django.views import View

from app.obj.forms import CreateHighlight
from app.obj.models import Highlight
from app.utils.db import conn


class IndexView(View):
    url_pattern = '<int:page>'
    name = 'index'

    def get(self, request, page):
        page = int(page)
        page_size_limit = 20
        page_start = (page - 1) * page_size_limit
        page_end = page * page_size_limit
        imgs = conn.get_cats_from_objects(Highlight.objects, page_start, page_end, ['comment'])
        return render(request, 'highlights.html', {
            'imgs': imgs,
            'page': page,
            'more_pages': len(conn.get_cats_from_objects(Highlight.objects, page_end, page_end+1, ['comment'])) != 0
            })

    def post(self, request, page):
        page = int(page)
        btn = request.POST['btn_submit']
        if btn == 'Next page':
            return redirect('highlights:index', page=page + 1)
        elif btn == 'Previous page':
            return redirect('highlights:index', page=page - 1)
        else:
            self.get(request, page)


class CreateView(View):
    url_pattern = 'create'
    name = 'create'

    def post(self, request):
        form = CreateHighlight(request.POST)
        if form.is_valid():
            form.save()
            print('saved')
        return redirect('highlights:index', page='1')
