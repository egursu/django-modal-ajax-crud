from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DeleteView


class AjaxContextData:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.kwargs
        [filter.pop(key, None) for key in ['pk', 'id', 'uuid', 'slug']]
        context['object_list'] = self.get_queryset().filter(**filter)
        return context

class AjaxValidForm:
    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['html_list'] = render_to_string(self.ajax_list, context, self.request)
        else:
            data['form_is_valid'] = False
        data['html_form'] = render_to_string(self.ajax_modal, context, request=self.request)
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
            context = self.get_context_data()
            data['html_list'] = render_to_string(self.ajax_list, context, self.request)
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)
