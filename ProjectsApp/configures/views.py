import os
import json
import logging
from datetime import datetime

from rest_framework.viewsets import ModelViewSet

from .models import ConfiguresModels
from .serializer import ConfiguresSerializer
# Create your views here.

loggers = logging.getLogger('TestcasesErrorLog')


class ConfiguresViewSet(ModelViewSet):
    queryset = ConfiguresModels.objects.all()
    serializer_class = ConfiguresSerializer
    # permission_classes = [permissions.IsAuthenticated]