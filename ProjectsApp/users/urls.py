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

from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views



urlpatterns = [
    path('login/', obtain_jwt_token),
    # path('register/', views.RegisterUserView.as_view()),
    path('register/', views.RegisterGetTokenViewSet.as_view({'post': 'create'})),
    re_path(r'^(?P<username>\w{6,20})/count/$', views.UserNameIsExistedView.as_view()),
    re_path(r'^(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/count/$',
            views.EmailIsExistedView.as_view()),
               ]
