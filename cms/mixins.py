from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from .utils import get_model_name, get_kwarg_object

class AjaxContextMixin:
    template = ''

    def dispatch(self, *args, **kwargs):
        self.model_name = get_model_name(self.model)
        self.app_name = self.model._meta.app_label
        self.model_verbose_name = get_model_name(self.model, 'verbose_name')
        self.model_verbose_name_plural = get_model_name(self.model, 'verbose_name_plural')
        if not hasattr(self, 'ajax_form'):
            self.ajax_form = 'cms/modal/{}.html'.format(self.template)
        if not hasattr(self, 'ajax_list'):
            self.ajax_list = '{}/partials/{}_list_partial.html'.format(self.app_name, self.model_name.lower())
        # self.template_name = self.ajax_form
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['model_name'] =  self.model_name
        context['app_name'] = self.app_name
        context['model_verbose_name'] = self.model_verbose_name
        context['model_verbose_name_plural'] = self.model_verbose_name_plural
        if hasattr(self, 'event'):
            context['title'] = self.event.capitalize() + ' ' + self.model_verbose_name.capitalize()
        else:
            context['title'] = self.model_verbose_name_plural.capitalize()
            if self.kwargs:
                for key, value in self.kwargs.items():
                    # context['title'] += ' of {}: {}'.format(get_model_name(key, 'verbose_name'), get_kwarg_object(key, value))
                    context['title'] += ' of {}'.format(get_kwarg_object(key, value))
        # context['object_list'] = self.get_queryset()
        context['kwargs'] = self.kwargs
        filter = self.kwargs
        [filter.pop(key, None) for key in ['pk', 'id', 'uuid', 'slug']]
        context['object_list'] = self.get_queryset().filter(**filter)
        return context


class AjaxObjectMixin:
    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_form, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)


class AjaxFormMixin:
    data = dict()

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save()
            if obj:
                self.data['form_is_valid'] = True
                self.data['html_list'] = render_to_string(self.ajax_list, context=self.get_context_data(), request=self.request)
                self.data['message'] = 'Successful saved.'
                if hasattr(self, 'success_url'):
                   self.data['redirect'] = self.success_url
            else:
                super().form_invalid(form)
            if self.request.is_ajax():
                return JsonResponse(self.data)
            else:
                return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        self.data['form_is_valid'] = False
        self.data['html_form'] = render_to_string(self.ajax_form, context=self.get_context_data(), request=self.request)
        self.data['message'] = 'Form validation error!'
        if self.request.is_ajax():
                return JsonResponse(self.data)
        else:
            return super().form_invalid(form)


class GetAbsoluteUrl:
    def get_absolute_url(self):
        model_name = self._meta.model_name.lower()
        app = self._meta.app_label
        return reverse_lazy("{}:{}-update".format(app, model_name), kwargs={'pk': self.pk})


class DynamicTemplateMixin:
    def get_template_names(self):
        view_template = ""
        if not hasattr(self, 'template'):
            raise AttributeError(
                "Add template attribute to your {}  for example if list view"
                " then add template='list' appropriate values"
                " list,detail,form,confirm_delete".format(self.__class__.__name__)
            )
        model_name = get_model_name(self.model).lower()
        app = self.model._meta.app_label
        view_template =  "{}/{}_{}.html".format(app, model_name, self.template)
        
        # if self.template == "list":
        #     model_name = self.model.__name__.lower()
        #     app = self.model._meta.app_label
        #     view_template =  "{}/{}_{}.html".format(app, model_name, self.template)
        # else:
        #     view_template =  "cms/modal/{}.html".format(self.template)
        return [view_template]

class SuccessUrlMixin:
    def get_success_url(self):
        model_name = get_model_name(self.model).lower()
        app = self.model._meta.app_label
        return reverse_lazy("{}:{}-list".format(app, model_name))


class BaseViewMixin(DynamicTemplateMixin, AjaxContextMixin):
    pass

class FormViewMixin(BaseViewMixin, SuccessUrlMixin, AjaxFormMixin):
    pass