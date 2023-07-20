"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime
from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'ProjectsApp'))
LOG_FILE_DIR = os.path.join(BASE_DIR, 'ProjectErrorLog', 'projectrunlog.log')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-axmclea_#7+&gs-u5z6oieesb@zelbc2wescxbb2n^g19b$3$p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# AUTH_USER_MODEL = 'projects.ProjectsModels'
# Application definition

INSTALLED_APPS = [
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django子类
    'rest_framework',
    'django_filters',
    # 子应用
    'projects',
    # 'apps',
    'interfaces',
    'users',
    'configures',
    'debugtalks',
    'envs',
    'reports',
    'testcases',
    'testsuits',
    'summary',

    # 外部插件
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'djangoProject',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# 在全局配置文件settings.py文件中的REST_FRAMEWORK字典里修改DRF框架的配置
REST_FRAMEWORK = {
    # 设置docs目录中的默认接口文档模板
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 'NON_FIELD_ERRORS_KEY': 'errors',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter'],
    # 为了灵活使用分页功能,可以使用重写然后使用的方法
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.MyPagination',

    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.pageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny'
        'rest_framework.permissions.IsAuthenticated'
    ],
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.jwt_handle.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
}
# 指定能够访问后端接口的ip或域名列表
CORS_ORIGIN_WHITELIST = [
                'http://127.0.0.1:*',
                'http://localhost:*',
                'http://192.168.66.238:8082',
                'http://192.168.120.121:8082',
                'http://192.168.0.105:8082'
            ]

CORS_ALLOW_CREDENTIALS = True

LOGGING = {
            # 版本号
            'version': 1,
            # 指定是否禁用已经存在的日志器,设置为True则禁用
            'disable_existing_loggers': False,
            # 日志的显示格式：formatters
            'formatters': {
                # simple为简化版格式的日志
                'simple': {
                    # 产生时间:asctime; 日志等级:levelname; msg:自定义;
                    'format': '%(asctime)s - [%(levelname)s] - [msg]%(message)s'
                },
                # verbose为详细格式的日志
                'verbose': {
                    # 产生错误的文件:filename; 产生错误的行数:lineno
                    'format': '%(asctime)s - [%(levelname)s] - %(name)s - [msg]%(message)s - [%(filename)s:%(lineno)d ]'
                },
            },
            # filters指定日志过滤器
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            # handlers指定日志输出渠道
            'handlers': {
                # console指定输出到控制台
                'console': {
                    'level': 'DEBUG',
                    # 日志过滤器中指定
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
                # file指定输出到日志,保存到日志文件
                'file': {
                    'level': 'DEBUG',
                    # RotatingFileHandler轮转日志(设定日志个数和大小,到达限制后自动删除最早文件)
                    'class': 'logging.handlers.RotatingFileHandler',
                    # 指定存放日志文件的所处路径
                    # 日志文件的位置(linux中可以使用var/log取代BASE_DIR进行拼接)
                    'filename': LOG_FILE_DIR,
                    'maxBytes': 100 * 1024 * 1024,  # 日志存储最大空间(100MB)
                    'backupCount': 10,  # 最大日志个数(10)
                    'formatter': 'verbose',
                    'encoding': 'utf-8'
                },
            },
            # 定义日志器
            'loggers': {
                'ProjectErrorLog': {  # 定义了一个名为ProjectErrorLog的日志器
                    'handlers': ['console', 'file'],
                    'propagate': True,
                    'level': 'DEBUG',  # 日志器接收的最低日志级别
                },
            }
        }


# 指定前端token值传递的前缀,不写默认是"JWT"
# JWT_AUTH_HEADER_PREFIX = 'JWT',

# JWT_EXPIRATION_DELTA: datetime.timedelta(days=1)

# 定义下载的报告的存放路径,变量名要大写
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
SUITES_DIR = os.path.join(BASE_DIR, 'suites')
DEBUGTALK_DIR = os.path.join(BASE_DIR, 'debugtalk.py')

