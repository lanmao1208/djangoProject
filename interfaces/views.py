from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InterfacesModels
from .serializer import InterfacesSerializer
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import json
# Create your views here.
class InterfacesView(GenericAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    def get(self, request):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        if page is not None:
            inter_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(inter_obj.data)
        inter_obj = self.get_serializer(instance=qs, many=True)
        return Response(inter_obj.data)

    def post(self, request):
        inter_obj = self.get_serializer(data=request.data)
        inter_obj.is_valid(raise_exception=True)
        inter_obj.save()
        return Response(inter_obj.data, status=status.HTTP_200_OK)



class InterfacesDetailView(GenericAPIView):

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    def get(self, request, pk):
        qs = self.get_object()
        inter_obj = self.get_serializer(instance=qs)
        return Response(inter_obj.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        qs = self.get_object()
        inter_obj = self.get_serializer(instance=qs, data=request.data)
        inter_obj.is_valid(raise_exception=True)
        inter_obj.save()
        return Response(inter_obj.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        qs = self.get_object()
        qs.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)