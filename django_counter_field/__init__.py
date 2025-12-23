"""Django counter field for tracking related model counts."""

from django_model_changes import ChangesMixin as CounterMixin

from ._version import __version__
from .counter import connect_counter
from .fields import CounterField

__all__ = ["CounterField", "CounterMixin", "connect_counter", "__version__"]
