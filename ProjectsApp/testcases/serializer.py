from rest_framework import serializers
from .models import TestcasesModels
from projects.models import ProjectsModels
from utils import common


class TestcasesSerializer(serializers.ModelSerializer):
    # project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=ProjectsModels.objects.all())

    class Meta:
        model = TestcasesModels
        fields = ('id', 'name', 'include', 'project_id', 'interface', 'author', 'request')
        extra_kwargs = {
            'include': {
                'write_only': True
            }
        }

    def validators_include(self, value):
        if type(value) != list:
            raise serializers.ValidationError('该字段必须为列表')
        # ***该方法必须返回value值***
        return value

    def create(self, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().create(validated_data)
        else:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().update(instance, validated_data)
        else:
            return super().update(instance, validated_data)




