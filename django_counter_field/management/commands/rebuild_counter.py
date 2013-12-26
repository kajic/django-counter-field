import sys

from django.core.management.base import BaseCommand, CommandError

from pomoji.django_counter_field.counter import counters

class Command(BaseCommand):
    args = '<counter_name>'
    help = 'Rebuilds the specified counter'

    def handle(self, *args, **options):
        if len(args) != 1:
            sys.exit("Usage: python manage.py rebuild_counter <counter_name>")
        counter_name = args[0]
        if not counter_name in counters:
            sys.exit("%s is not a registered counter" % counter_name)

        counter = counters[counter_name]

        seen_ids = set()
        count = 0
        current_referenced_id = 0
        for instance in counter.counted_model.objects.all().order_by(*[counter.foreign_field_name]):
            referenced_id = counter.referenced_id(instance)
            seen_ids.add(referenced_id)

            # We are iterating the counted objects in foreign field order and every time
            # the referenced id changes we will save the counter and prepare for
            # the next batch of counted objects (i.e. reset count and current_referenced_id).
            if referenced_id != current_referenced_id:
                if current_referenced_id > 0:
                    counter.reset(last_instance)
                    if count > 0:
                        counter.increment(last_instance, count)

                # Reset counter and current id
                count = 0
                current_referenced_id = referenced_id

            if counter.is_in_counter(instance):
                count += 1

            # Keep track of the last instance so that we can save the counter once we encounter
            # the next group of instances
            last_instance = instance

        # Reset all counters that were not touched by the previous loop.
        # These are counters that no longer have any counted objects.
        counter.referenced_model.objects.exclude(**{
            counter.referenced_field()+"__in": seen_ids,
            counter.counter_name: 0
        }).update(**{
            counter.counter_name: 0
        })



