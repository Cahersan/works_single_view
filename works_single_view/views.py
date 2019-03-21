from rest_framework import generics

from .serializers import WorksSerializer


class CreateWorksAPIView(generics.CreateAPIView):
    serializer_class = WorksSerializer


class ListCreateWorksAPIView(generics.ListCreateAPIView):
    serializer_class = WorksSerializer


class RetrieveWorksAPIView(generics.RetrieveAPIView):
    serializer_class = WorksSerializer


class UpdateWorksAPIView(generics.UpdateAPIView):
    serializer_class = WorksSerializer


class DeleteWorksAPIView(generics.DestroyAPIView):
    serializer_class = WorksSerializer
