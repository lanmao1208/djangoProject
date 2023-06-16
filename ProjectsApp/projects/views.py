import logging
import os
import datetime

from djangoProject import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count

from .models import ProjectsModels
from .serializer import ProjectsSerializer, ProjectsNameSerializer, ProjectToInterfacesSerializer, ProjectsRunSerializer
from testsuits.models import TestsuitsModels
from interfaces.models import InterfacesModels
from envs.models import EnvsModels
from testcases.models import TestcasesModels
from utils import common

# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = ProjectsModels.objects.all()
    serializer_class = ProjectsSerializer

    ordering_fields = ['id', 'name']

    def list(self, request, *args, **kwargs):
        data_list = []
        response = super().list(request, *args, **kwargs)
        result = response.data['results']

        for item in result:
            project_id = item.get('id')
            # 获取指定项目下的所有接口的测试用例嵌套字典列表
            interface_testcase_qs = InterfacesModels.objects.values('id').annotate(testcases=Count('testcases'))\
                .filter(project_id=project_id)

            # 获取项目下的接口总数
            interfaces_count = interface_testcase_qs.count()

            # 定义初始用例总数为0
            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')

            # 获取项目下的配置总数
            interface_configure_qs = InterfacesModels.objects.values('id').annotate(configures=Count('configures'))\
                .filter(project_id=project_id)
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
        # return self.list(request, *args, **kwargs)
        # 避免分页操作,所以不用父类的list方法
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

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
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['interfaces']
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = EnvsModels.objects.filter(id=env_id).first()

        interface_qs = InterfacesModels.objects.filter(project=instance)
        if not interface_qs.exists():
            data = {
                'ret': False,
                'msg': '此项目下无接口，无法运行'
            }
            return Response(data, status=400)

        runnable_testcase_obj = []
        for interface_obj in interface_qs:
            # 当前接口项目的用例所在查询集对象
            testcase_qs = TestcasesModels.objects.filter(interface=interface_obj)
            if testcase_qs.exists():
                # 将两个列表合并
                runnable_testcase_obj.extend(list(testcase_qs))

        if len(runnable_testcase_obj) == 0:
            data = {
                'ret': False,
                'msg': '此项目下无用例，无法运行'
            }
            return Response(data, status=400)

        for testcase_obj in runnable_testcase_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 运行用例（生成报告）
        # common.run_testcase(instance, testcase_dir_path)
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNameSerializer
        elif self.action == 'interfaces':
            return ProjectToInterfacesSerializer
        elif self.action == 'run':
            return ProjectsRunSerializer
        else:
            return self.serializer_class
