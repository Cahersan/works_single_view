import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Work(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_id = models.IntegerField()
    title = models.TextField(max_length=50)
    contributors = ArrayField(models.TextField(max_length=50))
    iswc = models.CharField(max_length=10)
    source = models.CharField(max_length=50)