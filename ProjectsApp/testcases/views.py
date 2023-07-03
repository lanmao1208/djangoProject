import os
import json
import logging
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from djangoProject.settings import SUITES_DIR

from .models import TestcasesModels
from . import serializer
from utils import handle_datas, common
from interfaces.models import InterfacesModels
from envs.models import EnvsModels
# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestcasesModels.objects.all()
    serializer_class = serializer.TestcasesModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """获取用例详情信息"""
        # Testcase对象
        testcase_obj = self.get_object()

        # 用例前置信息,使用json转换避免转换中参数出现格式错误(eval)
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')

        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        testcase_request_data = testcase_request.get('test').get('request')

        # 处理用例的validate列表
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为[{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_data.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_data.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_data = testcase_request_data.get('data')
        testcase_form_data_list = handle_datas.handle_data6(testcase_form_data)

        # 处理json数据
        # testcase_json_data = str(testcase_request_data.get('json'))
        testcase_json_data = json.dumps(testcase_request_data.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract_data = testcase_request.get('test').get('extract')
        testcase_extract_data_list = handle_datas.handle_data3(testcase_extract_data)

        # 处理parameters数据
        testcase_parameters_data = testcase_request.get('test').get('parameters')
        testcase_parameters_data_list = handle_datas.handle_data3(testcase_parameters_data)

        # 处理setupHooks数据
        testcase_setup_hooks_data = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_data_list = handle_datas.handle_data5(testcase_setup_hooks_data)

        # 处理teardownHooks数据
        testcase_teardown_hooks_data = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_data_list = handle_datas.handle_data5(testcase_teardown_hooks_data)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = InterfacesModels.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')

        data = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": testcase_request_data.get('method'),
            "url": testcase_request_data.get('url'),
            "param": testcase_params_list,
            "header": testcase_headers_list,
            "variable": testcase_form_data_list,  # form表单请求数据
            "jsonVariable": testcase_json_data,

            "extract": testcase_extract_data_list,
            "validate": testcase_validate_list,
            "globalVar": testcase_variables_list,  # 变量
            "parameterized": testcase_parameters_data_list,
            "setupHooks": testcase_setup_hooks_data_list,
            "teardownHooks": testcase_teardown_hooks_data_list,
        }
        return Response(data)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)

        env = EnvsModels.objects.filter(id=env_id).first()
        # 生成yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)

        # 运行用例（生成报告）
        # common.run_testcase(instance, testcase_dir_path)
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'run':
            return serializer.TestcasesRunSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializers):
        # 通过重写该方法,可以调用create方法帮助我们进行数据校验
        if self.action == 'run':
            pass
        else:
            serializers.save()
