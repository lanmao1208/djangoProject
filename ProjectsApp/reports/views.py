from .models import ReportsModels
from .serializer import ReportsSerializer
from .utils import get_file_content
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
import os
import logging
# Create your views here.

loggers = logging.getLogger('ReportErrorLog')


class ReportsViewSet(GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin):
    queryset = ReportsModels.objects.all()
    serializer_class = ReportsSerializer

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        result = data['results']
        data_list = []
        for item in result:
            item.pop('summary')
            if item['result']:
                item['result'] = 'pass'
            else:
                item['result'] = 'false'
            data_list.append(item)
        data['results'] = data_list
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)
        result = data.data
        summary = result['summary']
        if 'true' in summary:
            summary = summary.replace('true', '1')
        if 'false' in summary:
            summary = summary.replace('false', '0')
        if 'null' in summary:
            summary = summary.replace('null', 'None')
        try:
            summary = eval(summary)
        except Exception as e:
            e.args = '内部参数错误'
            raise e
        result['summary'] = summary
        data.data = result
        return data

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取html文件
        instance = self.get_object()
        html_data = instance.html
        html_name = instance.name

        # 获取报告文件存放路径
        reports_dir = os.path.join(settings.REPORTS_DIR, html_name) + '.html'
        # 如果文件不存在指定目录下
        if not os.path.exists(reports_dir):
            # 将获取到的文件写入指定的文件中
            with open(reports_dir, 'w', encoding='utf-8') as file:
                file.write(html_data)
        # 对文件名进行中文转码,避免乱码
        name = escape_uri_path(html_name + '.html')
        # 将获取的文件流返回给前端（仅限chrome使用不报错）
        # return StreamingHttpResponse(get_file_content(reports_dir))
        response = StreamingHttpResponse(get_file_content(reports_dir))
        # 添加响应头,直接用Response对象[响应头名称] = 值
        # 下面两个响应头是下载文件必备参数
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{name}"
        return response