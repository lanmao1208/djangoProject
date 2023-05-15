from rest_framework import serializers
from interfaces.models import InterfacesModels
from projects.models import ProjectsModels
from rest_framework import validators



class InterfacesSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    Project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', write_only=True,queryset=ProjectsModels.objects.all())

    class Meta:
        model = InterfacesModels
        fields = '__all__'

    def create(self, validated_data):
        # 转换Project_id然后输出
        return InterfacesModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新所有非read_only字段
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name') or instance.name
        instance.projects_id = validated_data.get('apps_id') or instance.projects_id
        instance.tester = validated_data.get('tester') or instance.tester
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance




