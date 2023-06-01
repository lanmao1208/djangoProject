from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import DebugTalksModels
from .serializer import DebugTalksSerializer,DebugTalkRsetrieveSerializer
from rest_framework.response import Response
import logging
# Create your views here.

loggers = logging.getLogger('DebugTalkErrorLog')


class DebugTalksViewSet(ModelViewSet):
    queryset = DebugTalksModels.objects.all()
    serializer_class = DebugTalksSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # 方法一,重写父类方法
    def retrieve(self, request, *args, **kwargs):
        results = self.get_object()
        data = {
            'id': results.id,
            'debugtalk': results.debugtalk
        }
        return Response(data)

    # # 方法二,添加一个序列化器类,然后指定调用retrieve使用
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return DebugTalkRsetrieveSerializer
    #     else:
    #         return self.serializer_class