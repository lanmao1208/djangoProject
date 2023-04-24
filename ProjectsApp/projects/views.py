from rest_framework import viewsets
from .models import ProjectsModels
from .serializer import ProjectsSerializer, ProjectsNameSerializer, ProjectToInterfacesSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import logging
import rest_framework_jwt


# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')
class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer

    filterset_fields = ['id', 'names']
    ordering_fields = ['id', 'names']

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        if page is not None:
            pro_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(pro_obj.data)
        pro_obj = self.get_serializer(instance=qs, many=True)
        return Response(pro_obj.data)

    @action(detail=True)
    def apps(self, request, *args, **kwargs):
        qs = self.get_object()
        pro_obj = AppsModels.objects.filter(projects=qs)
        page = self.paginate_queryset(pro_obj)
        if page is not None:
            pro_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(pro_obj.data)
        pro_obj = self.get_serializer(instance=qs, many=True)
        loggers.debug(pro_obj.data)
        return Response(pro_obj.data)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNameSerializer
        elif self.action == 'interfaces':
            return ProjectToInterfacesSerializer
        else:
            return self.serializer_class
