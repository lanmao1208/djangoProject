from rest_framework import serializers
from .models import DebugTalksModels


class DebugTalksSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(help_text='所属项目信息')

    class Meta:
        model = DebugTalksModels
        fields = ('id', 'name', 'debugtalk', 'project')
        read_only_fields = ('name', 'project')
        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }


class DebugTalkRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebugTalksModels
        fields = ('id', 'debugtalk')





