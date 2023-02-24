from rest_framework import serializers
from projects.models import ProjectsModels
from rest_framework import validators

# class ProjectsSerializer(serializers.Serializer):
#     names =serializers.CharField(max_length=60, min_length=2, label='项目名称', help_text='项目名称',
#                                  validators=[validators.UniqueValidator(queryset=ProjectsModels.objects.all(),message='该项目已存在')])
#     leader = serializers.CharField(max_length=100, label='项目负责人', help_text='项目负责人')
#     leader_phone = serializers.CharField(max_length=60, label='项目负责人电话', required=False)
#     testers = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', required=False)
#     programmer = serializers.CharField(max_length=200, label='开发人员', help_text='开发人员', required=False)
#     project_states = serializers.CharField(max_length=60, label='项目状态', help_text='结束:0;进行中:1;暂停:2')


class ProjectsSerializer(serializers.ModelSerializer):
    # 对于时间进行格式化
    create_time = serializers.DateTimeField(format = "%Y-%m-%d %H:%M:%S", required = False)
    update_time = serializers.DateTimeField(format = "%Y-%m-%d %H:%M:%S", required = False)
    class Meta:
        model = ProjectsModels
        fields = '__all__'

    def create(self, validated_data):
        return ProjectsModels.objects.create(**validated_data)

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


