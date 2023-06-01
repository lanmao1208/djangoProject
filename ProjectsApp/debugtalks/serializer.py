from rest_framework import serializers
from .models import DebugTalksModels
from utils import common


class DebugTalksSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')

    class Meta:
        model = DebugTalksModels
        fields = ('id', 'name', 'debugtalk', 'project')
        # extra_kwargs = {
        #     'name': {
        #
        #     }
        # }


class DebugTalkRsetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebugTalksModels
        fields = ('id', 'debugtalk')





