import sys

from django.core.management.base import BaseCommand
from django.db.models import Count

from django_counter_field.counter import counters


class Command(BaseCommand):
    args = '<counter_name>'
    help = """
    Rebuild the specified counter. Use python manage.py list_counters
    for a list of available counters.
    """

    def handle(self, *args, **options):
        if len(args) != 1:
            sys.exit("Usage: python manage.py rebuild_counter <counter_name>")

        counter_name = args[0]
        if not counter_name in counters:
            sys.exit("%s is not a registered counter" % counter_name)

        counter = counters[counter_name]

        parent_field = counter.foreign_field.name
        for parent in counter.parent_model.objects.all():
            parent_id = parent.id
            count = counter.child_model.objects.filter(**{ parent_field:parent_id}).count()
            counter.set_counter_field(parent_id, count)
