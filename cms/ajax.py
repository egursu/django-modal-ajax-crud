from django.http import JsonResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.apps import apps
from django.urls import resolve
import json


class AjaxContextData:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.kwargs
        [filter.pop(key, None) for key in ['pk', 'id', 'uuid', 'slug']]
        # context['object_list'] = self.get_queryset().filter(**filter)
        context['%s_list' % self.model.__name__.lower(
        )] = self.get_queryset().filter(**filter)
        return context


class AjaxValidForm:
    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['form_id'] = form.instance._meta.model_name
            data['html_list'] = render_to_string(
                self.ajax_list, context, self.request)
            data['message'] = 'Successful saved.'
        else:
            data['form_is_valid'] = False
            data['message'] = 'Form validation error!'
        data['html_form'] = render_to_string(
            self.ajax_modal, context, request=self.request)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return super().form_valid(form)


class AjaxCreateView(AjaxContextData, AjaxValidForm, CreateView):
    def get(self, request, *args, **kwargs):
        self.initial = self.kwargs
        self.object = None
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_modal, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)


class AjaxUpdateView(AjaxContextData, AjaxValidForm, UpdateView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_modal, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)


class AjaxDeleteView(AjaxContextData, DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_modal, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            data = dict()
            data['form_is_valid'] = True
            data['form_id'] = self.object._meta.model_name
            data['message'] = 'Successful deleted.'
            context = self.get_context_data()
            data['html_list'] = render_to_string(
                self.ajax_list, context, self.request)
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)


class AjaxReorderView(View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            data = dict()
            try:
                list = json.loads(self.request.body)
                if ':' in self.kwargs['model']:
                    app_model = self.kwargs['model'].split(':', 1)
                    app_name = app_model[0]
                    model_name = app_model[1]
                else:
                    app_name = resolve(self.request.path).app_name
                    model_name = self.kwargs['model']
                model = apps.get_model(app_name, model_name)
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
