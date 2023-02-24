from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectsModels
from .serializer import ProjectsSerializer
from django.http import JsonResponse
import json
# Create your views here.

class ProjectsView(APIView):

    def get(self, request):
        qs = ProjectsModels.objects.all()
        pro_obj = ProjectsSerializer(instance=qs, many=True)
        return Response(pro_obj.data, status=status.HTTP_200_OK)

    def post(self, request):
        msg = {}
        pro_obj = ProjectsSerializer(data=request.data)
        try:
            pro_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        pro_obj.save()
        msg.update(pro_obj.data)
        return Response(msg, status=status.HTTP_201_CREATED)

class ProjectsDetailView(APIView):
    def get(self, request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        pro_obj = ProjectsSerializer(instance=qs)
        msg.update(pro_obj.data)
        return Response(msg, status=status.HTTP_200_OK)

    def put(self, request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        pro_obj = ProjectsSerializer(instance=qs, data=request.data)
        try:
            pro_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        pro_obj.save()
        msg.update(pro_obj.data)
        return Response(msg, status=status.HTTP_201_CREATED)

    def delete(self,request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        msg["message"] = "删除成功"
        msg["code"] = 0
        return Response(msg, status=status.HTTP_204_NO_CONTENT)