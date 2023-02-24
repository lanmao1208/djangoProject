from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InterfacesModels
from .serializer import InterfacesSerializer
from django.http import JsonResponse
import json
# Create your views here.
class InterfacesView(APIView):

    def get(self, request):
        qs = InterfacesModels.objects.all()
        interfaces_obj = InterfacesSerializer(instance=qs, many=True)
        return Response(interfaces_obj.data, status=status.HTTP_200_OK)

    def post(self, request):
        msg = {}
        inter_obj = InterfacesSerializer(data=request.data)
        try:
            inter_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        inter_obj.save()
        msg.update(inter_obj.data)
        return Response(msg, status=status.HTTP_200_OK)



class InterfacesDetailView(APIView):
    def get(self, request, pk):
        msg = {}
        try:
            qs = InterfacesModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        interfaces_obj = InterfacesSerializer(instance=qs)
        msg.update(interfaces_obj.data)
        return Response(msg, status=status.HTTP_200_OK)

    def put(self, request, pk):
        msg = {}
        try:
            qs = InterfacesModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        pro_obj = InterfacesSerializer(instance=qs, data=request.data)
        try:
            pro_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        pro_obj.save()
        msg.update(pro_obj.data)
        return Response(msg, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        msg = {}
        try:
            qs = InterfacesModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        qs.delete()
        msg["message"] = "删除成功"
        msg["code"] = 0
        return Response(msg, status=status.HTTP_204_NO_CONTENT)