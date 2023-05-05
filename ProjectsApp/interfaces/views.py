from .models import InterfacesModels
from .serializer import InterfacesSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
# Create your views here.


class InterfacesViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'name', 'project_id']
    ordering_fields = ['id', 'name', 'project_id']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)