from rest_framework import serializers
from projects.models import ProjectsModels
from utils import common
from interfaces.models import InterfacesModels
from debugtalks.models import DebugTalksModels


class ProjectsSerializer(serializers.ModelSerializer):
    # 对于时间进行格式化
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = ProjectsModels
        # fields = '__all__'
        # fields = ('id', 'name', 'leader', 'tester', 'create_time', 'programmer')
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }
        }

    def create(self, validated_data):
        project = super().create(validated_data)
        DebugTalksModels.objects.create(project=project)
        return project

    def update(self, instance, validated_data):
        """
        更新所有非read_only字段
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name') or instance.name
        instance.leader = validated_data.get('leader') or instance.leader
        instance.tester = validated_data.get('tester') or instance.tester
        instance.programmer = validated_data.get('programmer') or instance.programmer
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance


class ProjectsNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsModels
        fields = ('id', 'name')

class InterfacesToProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterfacesModels
        fields = ('id', 'name')

class ProjectToInterfacesSerializer(serializers.ModelSerializer):

    interfaces = InterfacesToProjectSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectsModels
        fields = ('id', 'name', 'interfaces')

