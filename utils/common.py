# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/8/1 10:49 
  @Auth : 可优
  @File : common.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import json
import locale
import os
import yaml
import logging

from debugtalks.models import DebugTalksModels
from configures.models import ConfiguresModels
from testcases.models import TestcasesModels

loggers = logging.getLogger('TestcasesRunLog')


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'


def generate_testcase_file(instance, env, testcase_dir_path):
    """
    结构目录
    suites/时间戳/项目名/接口名/用例名.yaml
    suites/时间戳/项目名/debugtalk.py
    suties/时间戳/项目名/.env
    该方法用来创建测试用例yaml文件
    :param instance:
    :param env:
    :param testcase_dir_path:
    :return:
    """
    testcase_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 获取include信息
    include = json.loads(instance.include, encoding='utf-8')
    # 获取request字段
    request = json.loads(instance.request, encoding='utf-8')
    # 获取用例所属接口名称
    interface_name = instance.interface.name
    # 获取用例所属项目名称
    project_name = instance.interface.project.name

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        # 生成debugtalk.py文件，放到项目根目录下
        debugtalk_obj = DebugTalksModels.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj else ''
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {"config":1,"testcases":[1,2,3]}
    if 'config' in include:
        config_id = include.get('config')
        config_obj = ConfiguresModels.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['request']['base_url'] = env.base_url if env else ''
            testcase_list[0] = config_request

    # 处理前置用例
    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = TestcasesModels.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue

            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)
    # with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
    #     yaml.dump(testcase_list, f, all_unicode=True)

    with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)

    loggers.debug(f'新增用例{os.path.join(testcase_dir_path, instance.name + ".yaml")}')

