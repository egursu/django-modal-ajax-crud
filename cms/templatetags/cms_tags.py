from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

register = template.Library()

# settings value
@register.simple_tag
def settings_value(name):
    return mark_safe(getattr(settings, name, ""))


@register.simple_tag(takes_context=True)
def create_title(context, format_string):
    model_name = context['model_verbose_name']
    return '{} {}'.format(format_string, model_name)


@register.simple_tag(takes_context=True)
def get_object_url(context, action, obj=None):
    model = context['model']
    kwargs = context['kwargs']
    app = model._meta.app_label
    lower_name = obj.__class__.__name__.lower() if obj else model.__name__.lower()
    url_string = '{}:{}-{}'.format(app, lower_name, action)
    if (hasattr(obj, 'pk')):
        kwargs.update({'pk': obj.pk})
    elif (hasattr(obj, 'uuid')):
        kwargs.update({'uuid': obj.uuid})
    elif (hasattr(obj, 'slug')):
        kwargs.update({'slug': obj.slug})
    elif (hasattr(obj, 'id')):
        kwargs.update({'id': obj.id})
    return reverse_lazy(url_string, kwargs=kwargs) 


@register.simple_tag(takes_context=True)
def get_model_name(context):
    model = context['model']
    return model.__name__.lower()


@register.simple_tag(takes_context=True)
def get_template_name(context, *args):
    model = context['model']
    app = model._meta.app_label
    lower_name = model.__name__.lower()
    template_name = "{}/partials/{}_list_partial.html".format(app,lower_name)
    return template_name

@register.filter(name='verbose_name')
def get_verbose_name(object, attr='verbose_name'):
    # attr = verbose_name | verbose_name_plural | model_name | object_name
    # or field name (ex: field:title)
    obj = object.model if hasattr(object, 'model') else object
    if ':' in attr and attr.split(':', 1)[0].lower() == 'field':
        field = attr.split(':', 1)[1]
        attr = 'verbose_name' if hasattr(
            obj._meta.get_field(field), 'verbose_name') else 'name'
        return getattr(obj._meta.get_field(field), attr) if obj else None
    else:
        attr = attr if hasattr(obj._meta, attr) else 'object_name'
        return getattr(obj._meta, attr) if obj else None


@register.simple_tag
def get_field_verbose_name(object, field):
    obj = object.model if hasattr(object, 'model') else object
    prop = obj._meta.get_field(field)
    attr = 'verbose_name' if hasattr(prop, 'verbose_name') else 'name'
    return getattr(prop, attr) if obj else None


register.filter('field_verbose_name', get_field_verbose_name)


# @register.filter(name='model_name')
# def get_model_name(object, with_app=True):
#     obj = object.model if hasattr(object, 'model') else object
#     return f'{obj._meta.app_label}:{obj._meta.model_name}' if with_app else obj._meta.model_name if obj else None