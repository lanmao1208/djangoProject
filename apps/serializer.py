from rest_framework import serializers
from apps.models import AppsModels



class AppsSerializer(serializers.ModelSerializer):
    # projects_id = ProjectsSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = AppsModels
        fields = '__all__'

    def create(self, validated_data):
        return AppsModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新所有非read_only字段
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name') or instance.name
        instance.projects_id = validated_data.get('projects_id') or instance.projects_id
        instance.tester = validated_data.get('tester') or instance.tester
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance


