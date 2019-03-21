from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll


class Command(BaseCommand):
    help = 'Imports works metadata from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', type=str, help='A csv file with works metadata in an appropriate format')

    def handle(self, *args, **options):
        filename = options['file']

        with open(filename) as file:

            try:
                pass
            except Poll.DoesNotExist:
                raise CommandError('file "%s" does not exist' % filename)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % filename))
