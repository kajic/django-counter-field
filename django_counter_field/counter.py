from django.db.models import F

from django_model_changes import post_change

from .fields import CounterField

counters = {}


class Counter(object):
    def __init__(self, counter_name, foreign_field, is_in_counter):
        self.counter_name = counter_name
        self.foreign_field = foreign_field.field
        if not is_in_counter:
            is_in_counter = lambda instance: True
        self.is_in_counter = is_in_counter

        # Reference to the model that is counted by the counter
        self.counted_model = self.foreign_field.model
        # Reference to the model that defines the counter field
        self.referenced_model = self.foreign_field.rel.to
        self.foreign_field_name = self.foreign_field.name

        self.connect()

    def validate(self):
        referenced_model_fields = self.referenced_model._meta.fields
        fields_dict = dict(zip([field.name for field in referenced_model_fields], referenced_model_fields))
        counter_field = fields_dict.get(self.counter_name)
        # todo: figure out why this doesn't work together with management commands:
        # counter_field, _, _, _ = self.referenced_model._meta.get_field_by_name(self.counter_name)
        if not isinstance(counter_field, CounterField):
            raise TypeError("%s should be a CounterField on %s, but is %s" % (
                self.counter_name, self.referenced_model, type(counter_field)))

    def connect(self):
        self.validate()

        def receiver(sender, instance, *args, **kwargs):
            was_in_counter = instance.was_persisted() and self.is_in_counter(instance.old_instance())
            is_in_counter = instance.is_persisted() and self.is_in_counter(instance)

            if not was_in_counter and is_in_counter:
                self.increment(instance, 1)
            elif was_in_counter and not is_in_counter:
                self.increment(instance, -1)
        self.receiver = receiver

        post_change.connect(self.receiver, sender=self.counted_model, weak=False)
        self.register()

    def register(self):
        name = self.name()
        for i in range(100):
            unique_name = "%s-%s" % (name, i)
            if unique_name not in counters:
                break
        counters[unique_name] = self

    def name(self):
        return "%s-%s" % (
            "%s.%s" % (self.counted_model._meta.module_name, self.foreign_field_name),
            self.counter_name
        )

    def referenced_id(self, instance):
        return getattr(instance, self.foreign_field.attname)

    def referenced_field(self):
        return self.foreign_field.rel.field_name

    def set_counter(self, instance, value):
        return self.referenced_model.objects.filter(**{
            self.referenced_field(): self.referenced_id(instance)
        }).update(**{
            self.counter_name: value
        })

    def increment(self, instance, amount):
        return self.set_counter(instance, F(self.counter_name)+amount)

    def reset(self, instance):
        return self.set_counter(instance, 0)


def connect_counter(counter_name, foreign_field, is_in_counter_func=None):
    return Counter(counter_name, foreign_field, is_in_counter_func)
