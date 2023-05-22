from .models import InterfacesModels
from rest_framework.response import Response
from testcases.models import TestcasesModels
from configures.models import ConfiguresModels
from .serializer import InterfacesSerializer, InterfacesToTestcasesSerializer, InterfacesToConfiguresSerializer
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

    def list(self, request, *args, **kwargs):
        # 需要获取用例总数和配置总数
        response = super().list(request, *args, **kwargs)
        result = response.data['results']
        data_list = []
        for item in result:
            interface_id = item.get('id')
            testcase_count = TestcasesModels.objects.filter(interface_id=interface_id).count()
            configures_count = ConfiguresModels.objects.filter(interface_id=interface_id).count()
            # item['project_id'] = item.get('project_id')
            item['testcases'] = testcase_count
            item['configures'] = configures_count

            data_list.append(item)
        response.data['results'] = data_list
        return response

    @action(detail=False)
    def testcase(self, request, *args, **kwargs):
        instance = self.get_object()
        test_obj = self.get_serializer(instance=instance)
        testcases = test_obj.data['testcases']
        return Response(testcases)

    @action(detail=False)
    def configure(self, request, *args, **kwargs):
        instance = self.get_object()
        conf_obj = self.get_serializer(instance=instance)
        configures = conf_obj.data['configures']
        return Response(configures)

    def get_serializer_class(self):
        if self.action == 'testcase':
            return InterfacesToTestcasesSerializer
        elif self.action == 'configure':
            return InterfacesToConfiguresSerializer
        else:
            return self.serializer_class