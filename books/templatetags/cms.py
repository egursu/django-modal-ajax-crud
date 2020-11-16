from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.filter(name='object_verbose_name')
def get_object_verbose_name(object):
    if hasattr(object, 'model'):
        object = object.model
    return object._meta.verbose_name
# register.filter('object_verbose_name', get_object_verbose_name)

@register.filter(name='object_verbose_name_plural')
def get_object_verbose_name_plural(object):
    if hasattr(object, 'model'):
        object = object.model
    return object._meta.verbose_name_plural


@register.simple_tag
def get_field_verbose_name(object, field):
    if hasattr(object, 'model'):
        object = object.model
    return object._meta.get_field(field).verbose_name
register.filter('field_verbose_name', get_field_verbose_name)