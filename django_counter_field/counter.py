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
        """
        Validate that this counter is defined on the parent model.
        """
        parent_model_fields = self.parent_model._meta.fields
        fields_dict = dict(zip([field.name for field in parent_model_fields], parent_model_fields))
        counter_field = fields_dict.get(self.counter_name)
        # todo: figure out why this doesn't work together with management commands:
        # counter_field, _, _, _ = self.parent_model._meta.get_field_by_name(self.counter_name)
        if not isinstance(counter_field, CounterField):
            raise TypeError("%s should be a CounterField on %s, but is %s" % (
                self.counter_name, self.parent_model, type(counter_field)))

    def receive_change(self, instance):
        """
        Called when child model instances are saved/destroyed. Increments/decrements the underlying counter based on
        weather the child was/is in the counter.
        """
        was_in_counter = instance.was_persisted() and self.is_in_counter(instance.old_instance())
        is_in_counter = instance.is_persisted() and self.is_in_counter(instance)
        if not was_in_counter and is_in_counter:
            self.increment(instance, 1)
        elif was_in_counter and not is_in_counter:
            self.increment(instance, -1)

    def connect(self):
        """
        Register a counter between a child model and a parent.
        """
        self.validate()

        receiver = lambda sender, instance, **kwargs: self.receive_change(instance)
        post_change.connect(receiver, sender=self.child_model, weak=False)

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
    """
    Register a counter between a child model and a parent. The parent must define a CounterField field called
    *counter_name* and the child must reference its parent using a ForeignKey *foreign_field*. Supply an optional
    callback function *is_in_counter_func* for fine grained control over which child instances that should be counted.

    counter_name              - The name of the counter. A CounterField field with this name must be defined on the
                                parent model.
    foreign_field             - A ForeignKey field defined on the counted child model. The foreign key must reference
                                the parent model.
    is_in_counter_func(child) - Given a *child* instance, is_in_counter_func must return True if the instance qualifies
                                to be counted, and False otherwise. This callback should not concern itself with
                                checking if the instance is deleted or not.
    """
    return Counter(counter_name, foreign_field, is_in_counter_func)
