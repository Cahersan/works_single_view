from io import StringIO
from wsgiref.util import FileWrapper

from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import WorksSerializer
from .models import Work
from .utils import import_from_csv, export_from_csv, import_work


class WorksViewSet(ModelViewSet):
    serializer_class = WorksSerializer
    queryset = Work.objects.all()

    def create(self, request):
        work = import_work(request.data)
        serialized = self.get_serializer(work).data

        return Response(serialized, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post', 'get'])
    def csv(self, request):

        if self.request.method == 'POST':
            csvfile = request.FILES['file'].file

            # As per: https://stackoverflow.com/questions/42292773/read-uploaded-file-with-csv-reader
            csvfile = StringIO(csvfile.read().decode('iso-8859-1'))

            import_from_csv(csvfile)

            return Response({'message': 'Successfully imported works from CSV file'})
        else:
            csvfile = export_from_csv()

            with open(csvfile, 'r') as data:
                return HttpResponse(FileWrapper(data), content_type='text/csv')
