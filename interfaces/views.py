from .models import InterfacesModels
from .serializer import InterfacesSerializer
from rest_framework import viewsets
# Create your views here.


class InterfacesViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'name', 'projects']
    ordering_fields = ['id', 'name', 'projects']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

