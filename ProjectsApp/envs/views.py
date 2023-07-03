from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import EnvsModels
from .serializer import EnvsSerializer, EnvsNameSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('ProjectErrorLog')


class EnvsViewSet(ModelViewSet):
    queryset = EnvsModels.objects.all()
    serializer_class = EnvsSerializer
    # permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        # 不需要分页
        qs = self.get_queryset()
        data = self.get_serializer(qs, many=True).data
        return Response(data)
        # 需要分页则使用父类方法
        # return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        # if self.action == 'names':
        #     return EnvsNameSerializer
        # else:
        #     return self.serializer_class

        # 三元运算 可以缩减代码量
        return EnvsNameSerializer if self.action == 'names' else self.serializer_class
