import logging
import os
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import TestsuitsModels
from .serializer import TestsuitsSerializer, TestsuitsReadSerializer
from envs.models import EnvsModels
from testcases.models import TestcasesModels
from interfaces.models import InterfacesModels
from djangoProject import settings
from utils import common

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
        interface_qs = InterfacesModels.objects.filter(project=instance.interface.project)
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
