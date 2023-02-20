from django.shortcuts import render
from django.views import View
from .models import ProjectsModels
from .serializer import ProjectsSerializer
from django.http import JsonResponse
import json
# Create your views here.

class ProjectsView(View):

    def get(self, request):
        qs = ProjectsModels.objects.all()
        pro_obj = ProjectsSerializer(instance=qs, many=True)
        return JsonResponse(pro_obj.data, status=200, safe=False)

    def post(self, request):
        msg = {}
        print(request)
        pro_data = request.body

        try:
            pro_create_date = json.loads(pro_data)
        except Exception as e:
            print(e)
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)

        pro_obj = ProjectsSerializer(data=pro_create_date)
        try:
            pro_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)
        pro_obj.save()
        msg.update(pro_obj.data)
        return JsonResponse(msg, status=200)

class ProjectsDetailView(View):
    def get(self, request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)

        pro_obj = ProjectsSerializer(instance=qs)
        msg.update(pro_obj.data)
        return JsonResponse(msg, status=200)

    def put(self, request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
            pro_update_data = json.loads(request.body)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)
        pro_obj = ProjectsSerializer(instance=qs, data=pro_update_data)
        try:
            pro_obj.is_valid(raise_exception=True)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)
        pro_obj.save()
        msg.update(pro_obj.data)
        return JsonResponse(msg, status=200)

    def delete(self,request, pk):
        msg = {}
        try:
            qs = ProjectsModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)
        qs.delete()
        msg["message"] = "删除成功"
        msg["code"] = 0
        return JsonResponse(msg, status=201)