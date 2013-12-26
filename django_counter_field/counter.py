from django.db.models import F

from django_model_changes import post_change

from .fields import CounterField

counters = {}


class Counter(object):
    def __init__(self, counter_name, foreign_field, is_in_counter):
        self.counter_name = counter_name
        self.foreign_field = foreign_field.field
        self.child_model = self.foreign_field.model
        self.parent_model = self.foreign_field.rel.to

        if not is_in_counter:
            is_in_counter = lambda instance: True
        self.is_in_counter = is_in_counter

        self.connect()

    def validate(self):
        referenced_model_fields = self.parent_model._meta.fields
        fields_dict = dict(zip([field.name for field in referenced_model_fields], referenced_model_fields))
        counter_field = fields_dict.get(self.counter_name)
        # todo: figure out why this doesn't work together with management commands:
        # counter_field, _, _, _ = self.referenced_model._meta.get_field_by_name(self.counter_name)
        if not isinstance(counter_field, CounterField):
            raise TypeError("%s should be a CounterField on %s, but is %s" % (
                self.counter_name, self.parent_model, type(counter_field)))

    def receive_change(self, instance):
        was_in_counter = instance.was_persisted() and self.is_in_counter(instance.old_instance())
        is_in_counter = instance.is_persisted() and self.is_in_counter(instance)
        if not was_in_counter and is_in_counter:
            self.increment(instance, 1)
        elif was_in_counter and not is_in_counter:
            self.increment(instance, -1)

    def connect(self):
        self.validate()

        receiver = lambda sender, instance, **kwargs: self.receive_change(instance)
        post_change.connect(receiver, sender=self.child_model, weak=False)

        self.register()

    def register(self):
        name = "%s-%s" % (
            "%s.%s.%s" % (self.parent_model._meta.module_name, self.child_model._meta.module_name, self.foreign_field.name),
            self.counter_name
        )
        counters[name] = self

    def set_counter_field(self, child, value):
        """
        Set the value of a counter field to *value* using a *child* instance to find the parent.
        """
        parent_id = getattr(child, self.foreign_field.attname)
        return self.parent_model.objects.filter(pk=parent_id).update(**{self.counter_name: value})

    def increment(self, child, amount):
        """
        Increment a counter using a *child* instance to find the the parent.
        """
        return self.set_counter_field(child, F(self.counter_name)+amount)


def connect_counter(counter_name, foreign_field, is_in_counter_func=None):
    return Counter(counter_name, foreign_field, is_in_counter_func)
