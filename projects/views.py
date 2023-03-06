from rest_framework import viewsets
from .models import ProjectsModels
from .serializer import ProjectsSerializer

# Create your views here.


class ProjectsViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer
