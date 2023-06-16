from rest_framework import serializers

from projects.models import ProjectsModels
from utils import common, validates
from interfaces.models import InterfacesModels
from debugtalks.models import DebugTalksModels


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsModels
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


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID',
                                      write_only=True, validators=[validates.is_exised_env_id])

    class Meta:
        model = ProjectsModels
        fields = ('id', 'env_id')
