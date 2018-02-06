from django.core.management.base import BaseCommand
from django_counter_field.counter import counters


class Command(BaseCommand):
    help = 'List all registered counters.'

    def handle(self, **kwargs):
        for i, counter_name in enumerate(counters.keys(), 1):
            print "%s. %s" % (i, counter_name)
