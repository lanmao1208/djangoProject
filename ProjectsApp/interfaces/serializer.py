from rest_framework import serializers
from interfaces.models import InterfacesModels
from projects.models import ProjectsModels
from utils import common



class InterfacesSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', write_only=True, queryset=ProjectsModels.objects.all())


    class Meta:
        model = InterfacesModels
        # fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }
        }

    def create(self, validated_data):
        # 转换Project_id然后输出
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        return super().create(validated_data)



