from rest_framework import serializers
from .models import TestsuitsModels
from projects.models import ProjectsModels
from interfaces.models import InterfacesModels
from utils import common
import re


def validators_include(value):
    # ^开头$结尾,\d+匹配一个或者多个字符的数字(1,11,111)
    # (,\d+)匹配,','号后跟随的一个或者多个字符的数字,'*'号表示匹配多次
    obj = re.match(r'^\[\d+(,\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式错误')
    else:
        # group():返回匹配全部内容
        data_list = obj.group()

        try:
            data_list = eval(data_list)
        except:
            raise serializers.ValidationError('参数格式错误')
        for item in data_list:
            # exists()：如果数据库中请求的参数有值则返回True
            if not InterfacesModels.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id:{item}在数据库中未找到')


class TestsuitsSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=ProjectsModels.objects.all())

    class Meta:
        model = TestsuitsModels
        fields = ('id', 'name', 'include', 'project', 'project_id', 'create_time', 'update_time')
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            },
            'update_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            },
            'include': {
                'validators': [validators_include]
            }
        }

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


class TestsuitsReadSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', queryset=ProjectsModels.objects.all())

    class Meta:
        model = TestsuitsModels
        fields = ('name', 'include',  'project_id')

