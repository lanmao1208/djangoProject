from rest_framework import serializers

from projects.models import ProjectsModels
from interfaces.models import InterfacesModels
from envs.models import EnvsModels


def is_exised_project_id(value):
    """
    校验项目id是否存在
    :param value:
    :return:
    """
    if not ProjectsModels.objects.filter(id=value).exists():
        raise serializers.ValidationError('项目id不存在')


def is_exised_interface_id(value):
    """
    校验接口id是否存在
    :param value:
    :return:
    """
    if not InterfacesModels.objects.filter(id=value).exists():
        raise serializers.ValidationError('接口id不存在')


def is_exised_env_id(value):
    """
    校验环境变量id是否存在
    :param value:
    :return:
    """
    if not EnvsModels.objects.filter(id=value).exists():
        raise serializers.ValidationError('环境变量ID不存在')
