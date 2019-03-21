import csv

from django.core.management.base import BaseCommand, CommandError
from works_single_view.models import Work


class Command(BaseCommand):
    help = 'Imports works metadata from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', type=str, help='A csv file with works metadata in an appropriate format')

    def handle(self, *args, **options):
        filename = options['file']

        try:
            with open(filename, 'r') as csvfile:

                # As per https://stackoverflow.com/questions/11349333/when-processing-csv-data-how-do-i-ignore-the-first-line-of-data
                # check if the file has a header
                has_header = csv.Sniffer().has_header(csvfile.read(1024))
                csvfile.seek(0)  # Rewind

                rows = csv.reader(csvfile, delimiter=',')

                # If there is a header, skip the first row
                if has_header:
                    next(rows)

                for row in rows:
                    Work.objects.create(
                        title=row[0],
                        contributors=row[1].split('|'),
                        iswc=row[2],
                        source=row[3],
                        source_id=row[4]
                    )

        except (IOError, OSError) as e:
            raise CommandError('File "%s" does not exist' % filename)

        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % filename))
