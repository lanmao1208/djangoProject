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
    names =serializers.CharField(max_length=60, min_length=2, label='项目名称', help_text='项目名称',
                                 validators=[validators.UniqueValidator(queryset=ProjectsModels.objects.all(),message='该项目已存在')])
    class Meta:
        model = ProjectsModels
        fields = '__all__'


