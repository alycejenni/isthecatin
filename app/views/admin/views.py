from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from app.utils import constants
from app.utils.db import conn

decorators = [login_required(login_url='login'), user_passes_test(lambda u: u.is_superuser)]


class IndexView(View):
    url_pattern = ''
    name = 'index'

    @method_decorator(decorators)
    def get(self, request):
        return render(request, 'admin/admin.html')


class BulkEditView(View):
    url_pattern = 'bulkedit/<int:page>'
    name = 'bulkedit'
    template = 'admin/bulkedit.html'

    @staticmethod
    def template_render(request, template, page, **kwargs):

        return render(request, template, kwargs)

    @method_decorator(decorators)
    def get(self, request, page='1'):
        page = int(page)
        page_start = constants.BULK_EDIT_PAGE_SIZE * (page - 1)
        return render(request, self.template, {
            'imgs': conn.cats(page_start, constants.BULK_EDIT_PAGE_SIZE),
            'page': page
            })

    @method_decorator(decorators)
    def post(self, request, page='1'):
        page = int(page)
        page_start = constants.BULK_EDIT_PAGE_SIZE * (page - 1)
        if 'display' in request.POST:
            items = []
            displaytype = request.POST['display']
            if displaytype == 'cats':
                items = conn.cats(page_start, constants.BULK_EDIT_PAGE_SIZE)
            elif displaytype == 'all':
                items = conn.custom_keys(page_start, constants.BULK_EDIT_PAGE_SIZE)
            elif displaytype == 'notcats':
                items = conn.notcats(page_start, constants.BULK_EDIT_PAGE_SIZE)
            return render(request, self.template, {
                'imgs': items,
                'displaytype': displaytype,
                'page': page
                })
        elif 'btn_submit' in request.POST:
            btn = request.POST['btn_submit']
            if btn == 'Next page':
                return redirect('catmin:bulkedit', page=page + 1)
            elif btn == 'Previous page':
                return redirect('catmin:bulkedit', page=page - 1)
            elif btn == 'No cats here':
                btn_method = conn.set_not_cat
            elif btn == 'Delete these':
                btn_method = conn.delete_key
            else:
                raise NotImplementedError
            if 'items' in request.POST:
                items = request.POST.getlist('items')
                for i in items:
                    try:
                        btn_method(i)
                    except:
                        pass
                return render(request, self.template, {
                    'imgs': conn.cats(page_start, constants.BULK_EDIT_PAGE_SIZE),
                    'page': page
                    })
