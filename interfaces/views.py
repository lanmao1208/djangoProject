from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InterfacesModels
from .serializer import InterfacesSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
# Create your views here.
class InterfacesView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)



class InterfacesDetailView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)

    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)

    def delete(self, request, *arg, **kwargs):
        return self.destroy(request, *arg, **kwargs)