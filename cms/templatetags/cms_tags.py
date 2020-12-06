from django import template


register = template.Library()


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


@register.filter(name='model_name')
def get_model_name(object, with_app=True):
    obj = object.model if hasattr(object, 'model') else object
    return '{}:{}'.format(obj._meta.app_label, obj._meta.model_name) if with_app else obj._meta.model_name if obj else None
