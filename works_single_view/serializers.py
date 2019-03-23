from rest_framework import serializers

from works_single_view.models import Work


class WorksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = ('uid', 'title', 'iswc', 'contributors', 'source', 'source_id')
