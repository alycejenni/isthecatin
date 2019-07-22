from django.shortcuts import redirect
from django.views import View

from app.utils import kitty
from app.views.history import HistoryView


class SetNotCat(View):
    url_pattern = r'^set/notcat/(?P<img>.*)$'
    name = 'set.notcat'

    def post(self, request, img):
        try:
            kitty.set_not_cat(img)
        except Exception as e:
            print(e)
        return redirect(HistoryView.name, page='1')


