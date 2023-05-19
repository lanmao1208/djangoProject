from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TestsuitsModels
from .serializer import TestsuitsSerializer, TestsuitsReadSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('TestsuitErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestsuitsModels.objects.all()
    serializer_class = TestsuitsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)

    # @action(detail=True)
    # def read(self, *args, **kwargs):
    #     return self.retrieve(*args, **kwargs)

    # @action(detail=True)
    # def read(self, *args, **kwargs):
    #     testsuit = self.retrieve(*args, **kwargs).data
    #     data = {
    #             'name': testsuit.name,
    #             'project_id': testsuit.project_id,
    #             'include': testsuit.include
    #         }
    #     return Response(data)
    #
    #
    # def get_serializer_class(self):
    #     if self.action == 'read':
    #         return TestsuitsReadSerializer
    #     else:
    #         return self.serializer_class
