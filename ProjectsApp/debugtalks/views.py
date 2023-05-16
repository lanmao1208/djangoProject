from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import DebugTalksModels
from .serializer import DebugTalksSerializer
import logging
# Create your views here.

loggers = logging.getLogger('DebugTalkErrorLog')


class DebugTalksViewSet(ModelViewSet):
    queryset = DebugTalksModels.objects.all()
    serializer_class = DebugTalksSerializer
    # permission_classes = [permissions.IsAuthenticated]
