import os
import csv

from .models import Work


def import_from_csv(csvfile):
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


def export_from_csv():

    here = os.path.dirname(os.path.abspath(__file__))

    with open(here + '/reports/works_metadata.csv', 'w') as csvfile:
        fieldnames = ['title', 'contributors', 'iswc', 'source', 'id']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for work in Work.objects.all():
            writer.writerow({
                'title': work.title,
                'contributors': "|".join(work.contributors),
                'iswc': work.iswc,
                'source': work.source,
                'id': work.source_id
            })

    return csvfile.name
