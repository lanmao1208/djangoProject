from rest_framework import viewsets
from .models import ProjectsModels
from testsuits.models import TestsuitsModels
from interfaces.models import InterfacesModels
from .serializer import ProjectsSerializer, ProjectsNameSerializer, ProjectToInterfacesSerializer
from rest_framework.decorators import action
from django.db.models import Count
import logging
# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer

    filterset_fields = ['id', 'name']
    ordering_fields = ['id', 'name']

    def list(self, request, *args, **kwargs):
        data_list = []
        response = super().list(request, *args, **kwargs)
        result = response.data['results']

        for item in result:
            project_id = item.get('id')
            # 获取指定项目下的所有接口的测试用例嵌套字典列表
            interface_testcase_qs = InterfacesModels.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=project_id)

            # 获取项目下的接口总数
            interfaces_count = interface_testcase_qs.count()

            # 定义初始用例总数为0
            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')

            # 获取项目下的配置总数
            interface_configure_qs = InterfacesModels.objects.values('id').annotate(configures=Count('configures')).filter(project_id=project_id)
            configures_count = 0
            for one_dict in interface_configure_qs:
                configures_count += one_dict.get('configures')

            # 获取项目下套件总数
            testsuites_count = TestsuitsModels.objects.filter(project_id=project_id).count()

            item['interfaces'] = interfaces_count
            item['testcases'] = testcases_count
            item['testsuits'] = testsuites_count
            item['configures'] = configures_count

            data_list.append(item)

            response.data['results'] = data_list

        return response

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        # qs = self.get_object()
        # pro_obj = InterfacesModels.objects.filter(project=qs)
        # page = self.paginate_queryset(pro_obj)
        # if page is not None:
        #     pro_obj = self.get_serializer(instance=page, many=True)
        #     return self.get_paginated_response(pro_obj.data)
        # pro_obj = self.get_serializer(instance=qs, many=True)
        # loggers.debug(pro_obj.data)
        # return Response(pro_obj.data)
        return self.retrieve(self, request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNameSerializer
        elif self.action == 'interfaces':
            return ProjectToInterfacesSerializer
        else:
            return self.serializer_class
