from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TestcasesModels
from .serializer import TestcasesSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('TestcasesErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestcasesModels.objects.all()
    serializer_class = TestcasesSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     data = {
    #         'name': instance.name,
    #         'project_id': instance.project_id,
    #         'interface_id': instance.interface_id
    #     }
    #     return Response(data)