from rest_framework import serializers
from .models import ConfiguresModels
from projects.models import ProjectsModels
import re
from utils import common


class ConfiguresSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', write_only=True,
                                                    queryset=ProjectsModels.objects.all())

    class Meta:
        model = ConfiguresModels
        exclude = ('update_time',)

