from rest_framework import serializers
from interfaces.models import InterfacesModels
from testcases.models import TestcasesModels
from configures.models import ConfiguresModels
from projects.models import ProjectsModels
from utils import common


class InterfacesSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', queryset=ProjectsModels.objects.all())

    class Meta:
        model = InterfacesModels
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }

        }

    def create(self, validated_data):
        if 'project_id' in validated_data:
            # 转换Project_id然后输出
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            # validated_data['project_id'] = project.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            # validated_data['project_id'] = project.id
        return super().update(instance, validated_data)


class TestcasesNameIdSerializer(serializers.ModelSerializer):
    # 获取子表中指定pk值下所有的id和name
    class Meta:
        model = TestcasesModels
        fields = ('id', 'name')


class InterfacesToTestcasesByIdSerializer(serializers.ModelSerializer):
    # 根据获取到的子表数据,使用设定的变量名作为key,导入的序列化器类作为value
    # 按照外键关系建立对应关系,并使用设置的fields值进行过滤
    testcases = TestcasesNameIdSerializer(many=True, read_only=True)

    class Meta:
        model = InterfacesModels
        fields = ('testcases',)


class ConfiguresNameIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfiguresModels
        fields = ('id', 'name')


class InterfacesToConfiguresByIdSerializer(serializers.ModelSerializer):
    configures = ConfiguresNameIdSerializer(many=True, read_only=True)

    class Meta:
        model = InterfacesModels
        fields = ('configures',)