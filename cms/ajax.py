from cms.utils import string_to_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import (CreateView, UpdateView, DeleteView, View)
from django.views.generic.detail import DetailView
from cms.mixins import (AjaxContextMixin, AjaxObjectMixin, AjaxFormMixin)
from cms.forms import DynamicForm
from .utils import get_kwarg_object
import json


class AjaxCreateView(AjaxContextMixin, AjaxObjectMixin, AjaxFormMixin, CreateView):
    def dispatch(self, *args, **kwargs):
        self.object = None
        self.event = 'create'
        self.template = 'form'
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.initial = self.kwargs
        return super().get(request, *args, **kwargs)


class AjaxUpdateView(AjaxContextMixin, AjaxObjectMixin, AjaxFormMixin, UpdateView):
    def dispatch(self, *args, **kwargs):
        self.event = 'update'
        self.template = 'form'
        return super().dispatch(*args, **kwargs)


class AjaxDeleteView(AjaxContextMixin, AjaxObjectMixin, DeleteView):
    def dispatch(self, *args, **kwargs):
        self.event = 'delete'
        self.template = 'confirm_delete'
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            data = dict()
            data['form_is_valid'] = True
            data['message'] = 'Successful deleted.'
            context = self.get_context_data()
            data['html_list'] = render_to_string(self.ajax_list, context, self.request)
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)


class AjaxDetailView(AjaxContextMixin, AjaxObjectMixin, DynamicForm, DetailView):
    def dispatch(self, *args, **kwargs):
        self.event = 'detail'
        self.template = 'detail'
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        context['form'] = form
        context['form_control'] = self.form_control if hasattr(self, 'form_control') else False
        return context


class AjaxReorderView(View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            data = dict()
            try:
                list = json.loads(self.request.body)
                model = string_to_model(self.kwargs['model'])
                objects = model.objects.filter(pk__in=list)
                # list = {k:i+1 for i,k in enumerate(list)}
                for object in objects:
                    object.order = list.index(str(object.pk)) + 1
                model.objects.bulk_update(objects, ['order'])
                # for key, value in enumerate(list):
                #     model.objects.filter(pk=value).update(order=key + 1)
                message = 'Successful reorder list.'
                data['is_valid'] = True
            # except KeyError:
            #     HttpResponseServerError("Malformed data!")
            except:
                message = 'Internal error!'
                data['is_valid'] = False
            finally:
                data['message'] = message
                return JsonResponse(data)
        else:
            return JsonResponse({"is_valid": False}, status=400)


class AjaxFilesUpload(AjaxContextMixin, CreateView):
    def dispatch(self, *args, **kwargs):
        self.object = None
        self.event = 'upload'
        self.template = 'upload'
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            data = dict()
            context = self.get_context_data()
            form = self.form_class(self.request.POST, self.request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                for key, value in kwargs.items():
                    setattr(instance, key, get_kwarg_object(key, value))
                instance.save()
                data['is_valid'] = True
                data['html_list'] = render_to_string(self.ajax_list, context=context, request=self.request)
            else:
                data['is_valid'] = False
            return JsonResponse(data)
        else:
            return JsonResponse({"is_valid": False}, status=400)