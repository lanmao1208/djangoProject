from rest_framework import serializers
from .models import EnvsModels
from projects.models import ProjectsModels
from utils import common



class EnvsSerializer(serializers.ModelSerializer):
    # StringRelatedField包含默认属性read_only=True
    project = serializers.StringRelatedField(label='所属项目信息', help_text='所属项目信息')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id', write_only=True, queryset=ProjectsModels.objects.all())


    class Meta:
        model = EnvsModels
        # fields = ('id', 'name', 'base_url', 'create_time', 'desc', 'project', 'project_id')
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }
        }



class EnvsNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnvsModels
        fields = ('id', 'name')





