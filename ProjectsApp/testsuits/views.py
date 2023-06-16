from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TestsuitsModels
from .serializer import TestsuitsSerializer, TestsuitsReadSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('TestsuitsErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestsuitsModels.objects.all()
    serializer_class = TestsuitsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # 也可以新增一个序列化类,参照debugtalk
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)
