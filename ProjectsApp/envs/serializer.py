from rest_framework import serializers
from .models import EnvsModels
from projects.models import ProjectsModels
from utils import common


class EnvsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnvsModels
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





