from django.db import models


class CounterField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        super(CounterField, self).__init__(*args, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^pomoji\.django_counter_field\.fields\.CounterField"])
