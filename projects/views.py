from django.shortcuts import render
from django.views import View
from .models import ProjectsModels
from .serializer import ProjectsSerializer
from django.http import JsonResponse
# Create your views here.

class ProjectsView(View):
    def get(self, request):
        qs = ProjectsModels.objects.all()
        pro_obj = ProjectsSerializer(instance=qs, many=True)
        return JsonResponse(pro_obj.data, status=200, safe=False)

    def post(self, request):
        pass

class ProjectsDetailView(View):
    def get(self, request, pk):
        qs = ProjectsModels.objects.get(pk)
        pro_obj = ProjectsSerializer(instance=qs)
        return JsonResponse(pro_obj.data, status=200)