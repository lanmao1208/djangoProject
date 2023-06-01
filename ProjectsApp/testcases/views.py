from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TestcasesModels
from interfaces.models import InterfacesModels
from .serializer import TestcasesSerializer
from rest_framework.response import Response
import logging
# Create your views here.

loggers = logging.getLogger('TestcasesErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestcasesModels.objects.all()
    serializer_class = TestcasesSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        result = response.data['results']
        date_list = []
        for item in result:
            interface = list(InterfacesModels.objects.filter(id=item.get('interface')))[0]
            data = {
                'name': item.get('name'),
                'project': interface.project.name,
                # 'project_id': interface.project.id,
                'interface': interface.name,
                # 'interface_id': interface.id,
                'author': item.get('author')
            }
            date_list.append(data)
        response.data['results'] = date_list
        return response