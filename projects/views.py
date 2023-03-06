from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import ProjectsModels
from .serializer import ProjectsSerializer

# Create your views here.

class ProjectsView(GenericAPIView):
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer

    def get(self, request):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        if page is not None:
            pro_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(data=pro_obj.data)


    def post(self, request):
        pro_obj = self.get_serializer(data=request.data)
        pro_obj.is_valid(raise_exception=True)
        pro_obj.save()
        return Response(pro_obj.data, status=status.HTTP_201_CREATED)

class ProjectsDetailView(GenericAPIView):
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer


    def get(self, request, pk):
        qs = self.get_object()
        pro_obj = ProjectsSerializer(instance=qs)
        return Response(pro_obj.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        qs = self.get_object()
        pro_obj = ProjectsSerializer(instance=qs, data=request.data)
        pro_obj.is_valid(raise_exception=True)
        pro_obj.save()
        return Response(pro_obj.data, status=status.HTTP_201_CREATED)

    def delete(self,request, pk):
        qs = self.get_object()
        qs.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)