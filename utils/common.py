# -*- coding: utf-8 -*-
import json
import locale
import os
import shutil
import yaml
import logging
import pytest
from datetime import datetime
from natsort import natsorted
from concurrent import futures

from djangoProject.settings import REPORTS_DIR, SUITES_DIR, DEBUGTALK_DIR
from rest_framework.response import Response
from httprunner import (HttpRunner, Config, Step, RunRequest, RunTestCase, make)

from debugtalks.models import DebugTalksModels
from configures.models import ConfiguresModels
from testcases.models import TestcasesModels
from reports.models import ReportsModels

loggers = logging.getLogger('ProjectErrorLog')


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'


# def create_report(runner_obj, report_name=None):
#     """
#     创建测试报告
#     :param runner:
#     :param report_name:
#     :return:
#     """
#     runner = runner_obj.get_summary()
#     time_stamp = int(runner["time"]["start_at"])
#     start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
#     runner['time']['start_datetime'] = start_datetime
#     # duration保留3位小数
#     runner['time']['duration'] = round(runner['time']['duration'], 3)
#     report_name = report_name if report_name else start_datetime
#     runner['html_report_name'] = report_name
#
#     for item in runner['details']:
#         for record in item['records']:
#             # try:
#             #     record['meta_datas']['data'][0]['response']['content'] = \
#             #         record['meta_datas']['data'][0]['response']['content'].decode('utf-8')
#             # except Exception as e:
#             #     loggers.error(e)
#             #     pass
#             # try:
#             #     record['meta_datas']['data'][0]['response']['cookies'] = eval(record['meta_datas']['data'][0]
#             #                                                                   ['response']['cookies'])
#             # except Exception as e:
#             #     loggers.error(e)
#             #     pass
#             try:
#                 request_body = record['meta_datas']['data'][0]['response']['body']
#                 if isinstance(request_body, bytes):
#                     record['meta_datas']['data'][0]['response']['body'] = request_body.decode('utf-8')
#             except Exception as e:
#                 loggers.error(e)
#                 pass
#     summary = json.dumps(runner, ensure_ascii=False)
#
#     report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
#     html_name = os.path.join(REPORTS_DIR, report_name)
#
#
#     # with open(report_path, encoding='utf-8') as stream:
#     #     reports = stream.read()
#
#     test_report = {
#         'name': report_name,
#         'result': runner.get('success'),
#         'success': runner.get('stat')['testcases']['success'],
#         'count': runner.get('stat')['testcases']['total'],
#         # 'html': reports,
#         'summary': summary
#         # 'summary': reports
#     }
#     report_obj = ReportsModels.objects.create(**test_report)
#
#     return report_obj.id


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
    testcase_list = {}

    configures_results = ConfiguresModels.objects.filter(id=json.loads(instance.include)['config'])
    try:
        # config = json.loads(list(configures_results)[0].request).get('config')
        configures_request = json.loads(list(configures_results)[0].request).get('config').get('request')
        config = {
            'config': {
                'name': instance.name,
                'base_url': env.base_url if env else '',
                'request': {
                    'header': configures_request['headers']
                }
            }
        }

    except Exception as e:
        loggers.error(e)
        config = {}
        pass

    testcase_list['config'] = config['config']

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
        with open(DEBUGTALK_DIR, 'w', encoding='utf-8') as f:
            f.write(debugtalk)

    testcase_interfaces_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_interfaces_dir_path):
        os.makedirs(testcase_interfaces_dir_path)

    # {"config":1,"testcases":[1,2,3]}
    if 'config' in include:
        config_id = include.get('config')
        config_obj = ConfiguresModels.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['base_url'] = env.base_url if env else ''
            testcase_list['config'] = config_request['config']

    testcase_list['teststeps'] = []
    # 处理前置用例
    if 'testcases' in include:
        for testcase_id in include.get('testcases'):
            testcase_obj = TestcasesModels.objects.filter(id=testcase_id).first()
            testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            validate = testcase_request['testcases'].pop('validate')
            testcase_request['testcases']['request']['validate'] = validate
            # if 'variables' in testcase_request['testcases']:
            #     variables = testcase_request['testcases'].pop('variables')
            #     testcase_request['testcases']['variables'] = variables[0]
            testcase_list['teststeps'].append = testcase_request['testcases']

    validate = request['testcases'].pop('validate')
    request['testcases']['request']['validate'] = validate
    # 把当前需要执行的用例追加到testcase_list最后
    if 'parameters' in request['testcases']:
        parameters = request['testcases'].pop('parameters')
        testcase_list['config']['parameters'] = parameters[0]
        testcase_list['teststeps'].append(request['testcases'])
    # if 'variables' in request['testcases']:
    #     variables = request['testcases'].pop('variables')
    #     request['testcases']['variables'] = variables[0]
    else:
        testcase_list['testcases'] = request['testcases']

    with open(os.path.join(testcase_interfaces_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)


def move_old_file():
    # 需要清理的目录
    dir_list = [REPORTS_DIR, SUITES_DIR]
    for dir_path in dir_list:
        # 获取目录中的所有文件和子目录
        files = os.listdir(dir_path)
        # 如果目录下文件大于5则进行自动删除操作
        while len(files) > 5:
            # 对文件按创建时间进行排序
            # files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)))
            files = natsorted(files)
            remove_file = files[0]
            shutil.rmtree(os.path.join(dir_path, remove_file))
            files.remove(remove_file)
    return True


# def run_testcase(instance, testcase_dir_path):
#     # 将测试用例以接口为单位划分任务目标
#     files = os.listdir(testcase_dir_path)[0]
#     files_dir = os.path.join(testcase_dir_path, files)
#     files_list = os.listdir(files_dir)
#     files_list.remove('debugtalk.py')
#     pytest_files_dir = make.main_make(files_list)
#     # 多线程运行
#     with futures.ThreadPoolExecutor(max_workers=40) as e:
#         f1 = e.submit(move_old_file,)
#         loggers.info(msg=r'文件清理{}'.format(f1.result()))
#         for pytest_case in pytest_files_dir:
#             f2 = e.submit(start_run_testcase, pytest_case)
#         return Response(f2.result())

def run_testcase(testcase_dir_path, Threads_number=10):
    # 将测试用例以接口为单位划分任务目标
    files_dir_list = testcases_file_list(testcase_dir_path)
    # 目前只支持单项目运行
    make.main_make(files_dir_list)
    repotr_dir = os.path.join(REPORTS_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
    repotrfile_dir = os.path.join(repotr_dir, 'report_html.html')
    pytest.main(
        [files_dir_list[0],  # 测试用例
         # 生成测试报告 生成assert存放的css文件和html文件
         "--html={}".format(repotrfile_dir),
         "--self-contained-html",  # 把css样式合并到html里 仅生成html文件
         '-n={}'.format(Threads_number)  # 多线程,线程数默认为40
         ])
    report_id = create_report(repotrfile_dir, report_name=files_dir_list[0])
    data = {
        "id": report_id
    }
    return Response(data, status=201)


def testcases_file_list(dir_path):
    files = os.listdir(dir_path)
    files[0] = os.path.join(dir_path, files[0])
    return files


def create_report(report_dir, report_name=None):
    with open(report_dir, 'r', encoding='utf-8') as f:
        report_data = f.read()

    test_report = {
        'name': report_name,
        'result': True,
        'success': 0,
        'count': 0,
        'html': report_data,
        'summary': " "
        # 'summary': reports
    }
    report_obj = ReportsModels.objects.create(**test_report)

    return report_obj.id