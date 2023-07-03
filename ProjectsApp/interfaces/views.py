import logging
import os
from datetime import datetime

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import InterfacesModels
from testcases.models import TestcasesModels
from configures.models import ConfiguresModels
from envs.models import EnvsModels
from interfaces import serializer
from utils import common
from djangoProject import settings


# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')


class InterfacesViewSet(viewsets.ModelViewSet):
    filterset_fields = ['id', 'name', 'project_id']
    ordering_fields = ['id', 'name', 'project_id']

    queryset = InterfacesModels.objects.all()
    serializer_class = serializer.InterfacesSerializer

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

    @action(methods=['get'], detail=True)
    def testcases(self, request, *args, **kwargs):
        # 自定义方法类
        # instance = self.get_object()
        # test_obj = self.get_serializer(instance=instance)
        # testcases = test_obj.data['testcases']
        # return Response(testcases)
        # 拓展父类方法(推荐)
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['testcases']
        return response

    @action(methods=['get'], detail=True)
    def configures(self, request, *args, **kwargs):
        # 自定义方法类
        # instance = self.get_object()
        # conf_obj = self.get_serializer(instance=instance)
        # configures = conf_obj.data['configures']
        # return Response(configures)
        # 拓展父类方法(推荐)
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['configures']
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

        testcase_objs = TestcasesModels.objects.filter(interface=instance)
        if not testcase_objs.exists():  # 如果此接口下没有用例, 则无法运行
            data = {
                'ret': False,
                'msg': '此接口下无用例, 无法运行'
            }
            return Response(data, status=400)

        for one_obj in testcase_objs:
            common.generate_testcase_file(one_obj, env, testcase_dir_path)

        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'testcases':
            return serializer.InterfacesToTestcasesByIdSerializer
        elif self.action == 'configures':
            return serializer.InterfacesToConfiguresByIdSerializer
        elif self.action == 'run':
            return serializer.InterfaceRunSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        if self.action == 'run':
            pass
        else:
            serializer.save()