import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


def default_alternate():
    return {
        'title': [],
        'iswc': [],
        'source': [],
        'source_id': []
    }


class Work(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=50)
    contributors = ArrayField(models.TextField(max_length=50))
    iswc = models.CharField(max_length=14)
    source = models.CharField(max_length=50)
    source_id = models.IntegerField()
    alternate = JSONField(default=default_alternate)

    def __str__(self):
        return self.title
