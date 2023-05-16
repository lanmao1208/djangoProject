from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import EnvsModels
from .serializer import EnvsSerializer, EnvsNameSerializer
from rest_framework import permissions
from rest_framework.decorators import action
# Create your views here.

class EnvsViewSet(ModelViewSet):
    queryset = EnvsModels.objects.all()
    serializer_class = EnvsSerializer
    # permission_classes = [permissions.IsAuthenticated]


    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNameSerializer
        else:
            return self.serializer_class
