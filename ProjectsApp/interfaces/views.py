from .models import InterfacesModels
from projects.models import ProjectsModels
from testcases.models import TestcasesModels
from configures.models import ConfiguresModels
from .serializer import InterfacesSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('InterfaceErrorLog')


class InterfacesViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'name', 'project_id']
    ordering_fields = ['id', 'name', 'project_id']

    queryset = InterfacesModels.objects.all()
    serializer_class = InterfacesSerializer

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # 需要获取用例总数和配置总数
        response = super().list(request, *args, **kwargs)
        result = response.data['results']
        data_list = []
        for item in result:
            interface_id = item.get('id')
            testcase_count = TestcasesModels.objects.filter(interface_id=interface_id).count()
            configures_count = ConfiguresModels.objects.filter(interface_id=interface_id).count()
            item['project_id'] = item.get('project_id')
            item['testcases'] = testcase_count
            item['configures'] = configures_count

            data_list.append(item)
        response.data['results'] = data_list
        return response