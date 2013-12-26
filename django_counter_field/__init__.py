# As a convenience, export ChangesMixin aliased as CounterMixin
from django_model_changes.changes import ChangesMixin as CounterMixin

from .counter import connect_counter
from .fields import CounterField