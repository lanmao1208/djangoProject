from .models import AppsModels
from .serializer import AppsSerializer
from rest_framework import viewsets
# Create your views here.


class AppsViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'name', 'projects']
    ordering_fields = ['id', 'name', 'projects']

    queryset = AppsModels.objects.all()
    serializer_class = AppsSerializer

