from django.shortcuts import redirect, render
from django.views import View

from app.obj.forms import CreateHighlight
from app.utils.db import conn


class IndexView(View):
    url_pattern = '<int:page>'
    name = 'index'

    def get(self, request, page):
        page = int(page)
        page_size_limit = 18
        page_start = (page - 1) * page_size_limit
        page_end = page * page_size_limit
        is_mod = request.user.groups.filter(name__in=['Moderators', 'Admin']).exists()
        return render(request, 'history.html', {
            'imgs': conn.cats(page_start, page_size_limit),
            'nomination_form': CreateHighlight(),
            'page': page,
            'more_pages': len(conn.cats(page_end, 1)) != 0,
            'is_mod': is_mod or request.user.is_superuser
            })

    def post(self, request, page):
        page = int(page)
        btn = request.POST['btn_submit']
        if btn == 'Next page':
            return redirect('history:index', page=str(page + 1))
        elif btn == 'Previous page':
            return redirect('history:index', page=str(page - 1))
        else:
            self.get(request, page)
