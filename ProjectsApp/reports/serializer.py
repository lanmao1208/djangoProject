from rest_framework import serializers
from .models import ReportsModels
from utils import common


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportsModels
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            },
            'html': {
                'write_only': True
            }
        }





