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
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            },
            'update_time': {
                'write_only': True,
                'format': common.datetime_fmt()
            }
        }

    def create(self, validated_data):
        # 转换Project_id然后输出
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        更新所有非read_only字段
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name') or instance.name
        instance.projects_id = validated_data.get('project_id') or instance.projects_id
        instance.tester = validated_data.get('tester') or instance.tester
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance




