from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from .models import ProjectsModels
from .serializer import ProjectsSerializer

# Create your views here.

class ProjectsView(generics.ListCreateAPIView):
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer

class ProjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer