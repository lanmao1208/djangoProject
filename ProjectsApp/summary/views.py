import os
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.db.models import Sum

from projects.models import ProjectsModels
from interfaces.models import InterfacesModels
from testcases.models import TestcasesModels
from testsuits.models import TestsuitsModels
from configures.models import ConfiguresModels
from envs.models import EnvsModels
from debugtalks.models import DebugTalksModels
from reports.models import ReportsModels
# Create your views here.

loggers = logging.getLogger('SummaryErrorLog.log')


class SummaryAPIView(APIView):
    """
    返回统计信息
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取统计信息
        """
        users = request.user

        user_info = {
            'username': users.username,
            'role': '管理员' if users.is_superuser else '普通用户',
            'date_joined': users.date_joined.strftime('%Y-%m-%d %H:%M:%S') if users.date_joined else '',
            'last_login': users.last_login.strftime('%Y-%m-%d %H:%M:%S') if users.last_login else '',
        }

        projects_count = ProjectsModels.objects.count()
        interfaces_count = InterfacesModels.objects.count()
        testcases_count = TestcasesModels.objects.count()
        testsuits_count = TestsuitsModels.objects.count()
        configures_count = ConfiguresModels.objects.count()
        envs_count = EnvsModels.objects.count()
        debug_talks_count = DebugTalksModels.objects.count()
        reports_count = ReportsModels.objects.count()

        run_testcases_success_count = ReportsModels.objects.aggregate(Sum('success'))['success__sum'] or 0
        run_testcases_all_count = ReportsModels.objects.aggregate(Sum('count'))['count__sum'] or 0

        if run_testcases_all_count:
            success_rate = int((run_testcases_success_count/run_testcases_all_count)*100)
            fail_rate = 100 - success_rate
        else:
            success_rate = 0
            fail_rate = 0

        statistics = {
            'projects_count': projects_count,
            'interfaces_count': interfaces_count,
            'testcases_count': testcases_count,
            'testsuits_count': testsuits_count,
            'configures_count': configures_count,
            'envs_count': envs_count,
            'debug_talks_count': debug_talks_count,
            'reports_count': reports_count,
            'success_rate': success_rate,
            'fail_rate': fail_rate,
        }

        return Response(data={
            'user': user_info,
            'statistics': statistics
        })