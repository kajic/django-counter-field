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
        parent_id = 0
        count = 0

        parent_field = counter.foreign_field.name
        for child in counter.child_model.objects.all().order_by(parent_field):
            current_parrent_id = counter.parent_id(child)

            if parent_id != current_parrent_id:
                if parent_id > 0:
                    counter.set_counter_field(parent_id, count)
                parent_id = current_parrent_id
                count = 0

            if counter.is_in_counter(child):
                count = count+1

        if parent_id > 0:
            counter.set_counter_field(parent_id, count)
