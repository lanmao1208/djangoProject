from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from users.serializer import RegisterSerializer


class RegisterGetTokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    注册接口,简化版
    """
    # queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # 注册接口权限放开,不然用户无法进行注册
    permission_classes = [permissions.AllowAny]

    filterset_fields = ['username', 'email', 'token']
    ordering_fields = ['username', 'email', 'token']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def logout(self, request, *args, **kwargs):
        auth.logout(request)


# class RegisterUserView(APIView):
#     """
#     注册接口,只继承APIView
#     """
#     # 注册接口权限放开,不然用户无法进行注册
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         # 创建用户
#         user_obj = RegisterSerializer(data=request.data)
#         user_obj.is_valid(raise_exception=True)
#         user_obj.save()
#         return Response(user_obj.data, status=status.HTTP_201_CREATED)


class UserNameIsExistedView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        usercount = User.objects.filter(username=username).count()
        user_dict = {
            'username': username,
            'count': usercount
        }
        return Response(user_dict)


class EmailIsExistedView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, email):
        emailcount = User.objects.filter(email=email).count()
        email_dict = {
            'username': email,
            'count': emailcount
        }
        return Response(email_dict)