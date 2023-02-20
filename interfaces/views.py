from django.shortcuts import render
from django.views import View
from .models import InterfacesModels
from .serializer import InterfacesSerializer
from django.http import JsonResponse
# Create your views here.
class InterfacesView(View):

    def get(self, request):
        qs = InterfacesModels.objects.all()
        interfaces_obj = InterfacesSerializer(instance=qs, many=True)
        return JsonResponse(interfaces_obj.data, status=200, safe=False)


class InterfacesDetailView(View):
    def get(self, request, pk):
        msg = {}
        try:
            qs = InterfacesModels.objects.get(pk)
        except Exception as e:
            msg["message"] = e
            msg["code"] = 1
            return JsonResponse(msg, status=204)

        interfaces_obj = InterfacesSerializer(instance=qs)
        msg.update(interfaces_obj.data)
        return JsonResponse(msg, status=200)