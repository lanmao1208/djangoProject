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
from datetime import datetime

from djangoProject.settings import REPORTS_DIR
from rest_framework.response import Response
from httprunner.api import HttpRunner
from httprunner.report import gen_html_report

from debugtalks.models import DebugTalksModels
from configures.models import ConfiguresModels
from testcases.models import TestcasesModels
from reports.models import ReportsModels

loggers = logging.getLogger('TestcasesRunLog')


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'


def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner['time']['duration'] = round(runner['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner['html_report_name'] = report_name

    for item in runner['details']:
        try:
            for record in item['records']:
                record['meta_datas']['response']['content'] = record['meta_datas']['response']['content']. \
                    decode('utf-8')
                record['meta_datas']['response']['cookies'] = dict(record['meta_datas']['response']['cookies'])

                request_body = record['meta_datas']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_datas']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    html_name = os.path.join(REPORTS_DIR, report_name + '.html')
    report_path = gen_html_report(runner, report_dir=html_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.get('success'),
        'success': runner.get('stat')['testcases']['success'],
        'count': runner.get('stat')['testcases']['total'],
        'html': reports,
        'summary': summary
        # 'summary': reports
    }
    report_obj = ReportsModels.objects.create(**test_report)
    return report_obj.id


def generate_testcase_file(instance, env, testcase_dir_path):
    """
    结构目录
    suites/时间戳/项目名/接口名/用例名.yaml
    suites/时间戳/项目名/debugtalk.py
    suites/时间戳/项目名/.env
    该方法用来创建测试用例yaml文件
    :param instance:
    :param env:
    :param testcase_dir_path:
    :return:
    """
    testcase_list = []

    configures_results = ConfiguresModels.objects.filter(id=json.loads(instance.include)['config'])
    try:
        config = json.loads(list(configures_results)[0].request).get('config')
        # configures_request = json.loads(list(configures_results)[0].request).get('config').get('request')
        # config = {
        #     'config': {
        #         'name': instance.name,
        #         'request': {
        #             'base_url': env.base_url if env else '',
        #             'header': configures_request.get('header')
        #         }
        #     }
        # }

    except Exception as e:
        loggers.error(e)
        config = {}
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
                loggers.error(e)
                continue

            testcase_list.append(testcase_request)

    # 把当前需要执行的用例追加到testcase_list最后
    testcase_list.append(request)

    with open(os.path.join(testcase_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)

    # loggers.debug(f'新增用例{os.path.join(testcase_dir_path, instance.name + ".yaml")}')


def run_testcase(instance, testcase_dir_path):
    # 1、运行用例
    runner = HttpRunner()
    try:
        summary = runner.run(testcase_dir_path)
    except Exception as e:
        loggers.error(e)
        res = {'ret': False, 'msg': '用例执行失败'}
        return Response(res, status=400)

    # 2、创建报告
    report_id = create_report(summary, instance.name)

    # 3、用例运行成功之后，需要把生成的报告id返回
    data = {
        'id': report_id
        # 'id': 1
    }
    return Response(data, status=201)
