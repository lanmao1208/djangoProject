from .models import InterfacesModels
from .serializer import InterfacesSerializer
from rest_framework import generics
from rest_framework import mixins
# Create your views here.
class InterfacesView(generics.ListCreateAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer




class InterfacesDetailView(generics.RetrieveUpdateDestroyAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer
