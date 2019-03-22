from rest_framework.viewsets import ModelViewSet

from .serializers import WorksSerializer
from .models import Work


class WorksViewSet(ModelViewSet):
    serializer_class = WorksSerializer
    queryset = Work.objects.all()
