import os
import csv
from django.db.models import Q

from .models import Work


def match(metadata):
    """
    Match conditions are: A work with the give ISWC exists or a work with
    the same title and contributors exist.
    """

    return Work.objects.filter(
        Q(iswc=metadata['iswc']) |
        Q(title=metadata['title'], contributors=metadata['contributors'])
    ).first()


def reconcile(work, metadata):
    """
    This is the reconciliation logic for each item of metadata:

    1. for title, iswc, source and source_id: If there was no previous value
    for the item, the new one is used. If there is already a value westore the
    data in the 'alternate' JSON field present in the Works model for further
    introspection by a human or a complex algorithm. As of now, it's important
    not to loose information.

    2. contributors: For contributors I opted for a merge of lists.
    """

    # 1.
    items = ['title', 'iswc', 'source', 'source_id']

    for item in items:
        if not getattr(work, item):
            setattr(work, item, metadata[item])

        if getattr(work, item) != metadata[item]:
            work.alternate[item].append(metadata[item])

    # 2.
    work.contributors.extend(x for x in metadata['contributors'] if x not in work.contributors)

    work.save()

    return work


def import_work(metadata):
    work = match(metadata)

    if work:
        # If it's an existing work, we rconcile it
        work = reconcile(work, metadata)
    else:
        # If it's a new work, we create it
        work = Work.objects.create(**metadata)

    return work


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
        import_work({
            'title': row[0],
            'contributors': row[1].split('|'),
            'iswc': row[2],
            'source': row[3],
            'source_id': row[4]
        })


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
