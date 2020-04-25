from django.shortcuts import redirect
from django.views import View

from app.utils import kitty


class SetNotCat(View):
    url_pattern = 'notcat'
    name = 'notcat'

    def post(self, request):
        img = request.POST.get('img', None)
        page = request.POST.get('page', 1)
        if img is not None:
            try:
                kitty.set_not_cat(img)
            except Exception as e:
                print(e)
        return redirect('history:index', page=page)

