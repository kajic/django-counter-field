from django.core.management.base import BaseCommand

from django_counter_field.counter import counters


class Command(BaseCommand):
    help = """
    Rebuild the specified counter. Use python manage.py list_counters
    for a list of available counters.
    """

    def add_arguments(self, parser):
        parser.add_argument("counter_name", type=str, help="Name of the counter to rebuild")

    def handle(self, *args, **options):
        counter_name = options["counter_name"]
        if counter_name not in counters:
            self.stderr.write(f"{counter_name} is not a registered counter")
            return

        counter = counters[counter_name]

        parent_field = counter.foreign_field.name
        objects = counter.parent_model.objects.all()
        total = objects.count()
        for i, parent in enumerate(objects, 1):
            if total > 1000 and i % 1000 == 0:
                self.stdout.write(f"{i} of {total}")
            parent_id = parent.id
            count = counter.child_model.objects.filter(**{parent_field: parent_id}).count()
            counter.set_counter_field(parent_id, count)
        self.stdout.write("Completed!")
