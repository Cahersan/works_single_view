from django.core.management.base import BaseCommand, CommandError

from works_single_view.utils import import_from_csv


class Command(BaseCommand):
    help = 'Imports works metadata from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', type=str, help='A csv file with works metadata in an appropriate format')

    def handle(self, *args, **options):
        filename = options['file']

        try:
            with open(filename, 'r') as csvfile:
                import_from_csv(csvfile)
        except (IOError, OSError) as e:
            raise CommandError('File "%s" does not exist' % filename)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % filename))
