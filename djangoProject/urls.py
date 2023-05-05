"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
	openapi.Info(
		title="API文档",  # 必传
		default_version = "v1",  # 必传
		description="这是一个美轮美奂的接口文档",
		terms_of_service="http://api.keyou.site",
		contact=openapi.Contact(email="XXX@qq.com"),
		license=openapi.License(name="BSD Lincense")
	),
	public=True,
	permission_classes=(permissions.AllowAny,),  # 权限类
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),name='schema-json'),
	path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
	path('api/', include('rest_framework.urls')),


    path('', include('projects.urls')),
    path('', include('interfaces.urls')),
	# path('', include('apps.urls')),
	# path('', include('configures.urls')),
	# path('', include('debugtalks.urls')),
	# path('', include('envs.urls')),
	# path('', include('reports.urls')),
	# path('', include('testcases.urls')),
	# path('', include('testsuits')),
	path('user/', include('users.urls')),
]

