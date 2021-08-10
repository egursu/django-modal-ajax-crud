from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import check_for_language
from django.utils import translation
from django.urls import translate_url
from django.conf import settings

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .mixins import BaseViewMixin, FormViewMixin


def handler_404(request, exception):
    return render(request, '404.html', {'title': ('404 Error Page')})

    
def handler_500(request):
    return render(request, '500.html', {'title': ('500 Error Page')})
    

def set_lang(request, lang):
    next_url = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(next_url)
    lang = lang if check_for_language(lang) else request.LANGUAGE_CODE
    next_trans = translate_url(next_url, lang)
    if next_trans != next_url:
        response = HttpResponseRedirect(next_trans)
    # translation.activate(lang)
    if hasattr(request, 'session'):
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response


class CoreListView(BaseViewMixin, ListView):
    template = ''
    ajax_partial = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'list'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        self.ajax_partial = '{}/partials/{}_form_partial.html'.format(self.app,self.model_name)
        return super().dispatch(*args, **kwargs)

class CoreDetailView(BaseViewMixin, DetailView):
    template = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'detail'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        return super().dispatch(*args, **kwargs)


class CoreCreateView(FormViewMixin, CreateView):
    pass


class CoreUpdateView(FormViewMixin, UpdateView):
    pass
