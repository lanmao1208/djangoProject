from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler



class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=20, min_length=6, label="确认密码", help_text="确认密码", write_only=True)
    token = serializers.CharField(label="Token", help_text="Token", read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'token')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'error_messages': {
                    "required": "该字段必传",
                    "max_length": "仅允许6-20个字符的密码",
                    "min_length": "仅允许6-20个字符的密码",
                }
            },
            'email': {
                # 用户模型中email属性拥有blank=True,所以此处为了符合需求,要设置required=True
                'required': True,
                'write_only': True,
                # 添加邮箱重复认证
                'validators': [validators.UniqueValidator(queryset=User.objects.all(), message="该邮箱已存在")],
            },
            'password': {
                'max_length': 20,
                'min_length': 6,
                'label': "密码",
                'help_text': "密码",
                'write_only': True,
                'error_messages': {
                    "required": "该字段必传",
                    "max_length": "仅允许6-20个字符的密码",
                    "min_length": "仅允许6-20个字符的密码",
                }
            }
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("输入的两次密码不一致")
        return attrs

    def create(self, validated_data):
        # 去除pwd_confirm
        validated_data.pop('password_confirm')
        # 加密密码 调用UserManager.create_user可以免去这一步
        # data['password'] = make_password(data['password'])
        # 调用父类方法,创建入库
        user = User.objects.create_user(**validated_data)
        # 创建token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # 将token赋值给uesr属性中的token
        user.token = token
        return user