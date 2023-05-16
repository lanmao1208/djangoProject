from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TestsuitsModels
from .serializer import TestsuitsSerializer
from projects.serializer import ProjectsNameSerializer
from rest_framework.decorators import action
import logging
# Create your views here.

loggers = logging.getLogger('TestsuitErrorLog')


class TestsuitsViewSet(ModelViewSet):
    queryset = TestsuitsModels.objects.all()
    serializer_class = TestsuitsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNameSerializer
        else:
            return self.serializer_class
