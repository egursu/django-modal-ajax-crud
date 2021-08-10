from django.contrib.contenttypes.models import ContentType

def string_to_model(model_name):
    ct = ContentType.objects.get(model=model_name.lower())
    return ct.model_class()

def get_model_name(model, attr=None):
    if isinstance(model, str):
        model = string_to_model(model)
    if attr:
        if hasattr(model._meta, attr):
            return getattr(model._meta, attr)
        elif attr == 'verbose_name_plural':
            return get_model_name(model, 'verbose_name')
        else:
            return model.__name__
    else:
        return model.__name__

def get_kwarg_object(model_name, pk):
    return string_to_model(model_name).objects.get(pk=pk)