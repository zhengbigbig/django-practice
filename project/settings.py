from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '=ij=9js^@-k)0bw!sd53zh8aeg$vm*46t#18bw0i+8fp2j+qux'

DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
# 安装应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp',
    'App02',
    'captcha',
    'rest_framework',
    'drf',
]
# 中间件
MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middleware.myApp.myMiddle.MyMiddle',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]
# 根路由
ROOT_URLCONF = 'project.urls'
# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'

# 数据库配置

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# 语言
LANGUAGE_CODE = 'zh-Hans'
# 时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# 是否使用国际标准时间，改为False，数据库存储的时间和当前时间一致
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

import os

STATIC_URL = '/static/'
# 普通文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# --------------- add ----------------

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': '',
    'prefix': 'session',
    'socket_timeout': 1
}

# 上传文件目录
MEDIA_ROOT = os.path.join(BASE_DIR, r'static/upload')

# 富文本
TINYMCE_DEFAULT_CONFIG = {
    # // General options
    'theme': "advanced",
    'width': '700',
    'height': '400'
}

# auth
AUTH_USER_MODEL = 'App02.User'
# captcha验证码设置
CAPTCHA_IMAGE_SIZE = (80, 45)  # 设置图片大小
CAPTCHA_LENGTH = 4  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)
# 输出格式: 输入框 验证码图片 隐藏域
CAPTCHA_OUTPUT_FORMAT = '%(text_field)s %(image)s %(hidden_field)s'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',
                           'captcha.helpers.noise_arcs',  # 线
                           'captcha.helpers.noise_dots')  # 点
# 随机字符验证码
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'

# 黑名单设置
BLACKLIST = []

# 数据库缓存配置
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_chache_table',
#     }
# }
# CACHE_MIDDLEWARE_SECONDS = 20  # 设置超时时间 20秒
# 文件缓存
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',  # 指定缓存使用的引擎
#         'LOCATION': '/var/tmp/django_cache',  # 指定缓存路径
#         'TIMEOUT': 300,  # 缓存超时时间（默认300秒，None表示永不过期
#         'OPTIONS': {
#             'MAX_ENTRIES': 300,  # 最大缓存记录的数量（默认300）
#             'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即： 1，默认3
#         }
#     }
# }
# redis缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 'LOCATION':'redis://:password@127.0.0.1:6379/1', # 缓存地址，@前面是redis密码，若无则空
        'LOCATION': 'redis://127.0.0.1:6379/1',

    }
}

# celery
from kombu import Queue, Exchange

# 设置Broker和backend
BROKER_URL = 'redis://127.0.0.1:6379/0'
# 将数据存放到redis1数据库，redis默认有16个数据库
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND = 'django-db'
INSTALLED_APPS += [
    'celery',
    'django_celery_results',
]

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化使用json
CELERY_RESULT_SERIALIZER = 'json'  # 结果反序列化为json
CELERY_ACCEPT_CONTENT = ['json']  # 分布式接受数据的类型为json
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 后端存储任务超过一天，则自动清理数据，单位为秒
CELERY_MAX_TASKS_PER_CHILD = 1000  # 每个worker执行了多少任务就会死掉，防止内存泄露
# 定时任务
CELERYBEAT_SCHEDULE = {
    'schedule-test': {
        'task': 'myApp.tasks.hello_celery',
        'schedule': timedelta(seconds=3),
        'args': (6,)

    }
}
# # 计划任务
# CELERYBEAT_SCHEDULE = {
#     'every-ten-second-run-my-task': {
#         'task': 'app名字.tasks.hello_celery',
#         'schedule': crontab(minute='01',hour='15'),
#         'args': (2,)
#
#     }
# }

# smtp邮箱服务
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '780357902@qq.com'
EMAIL_HOST_PASSWORD = 'ezjmbexhlixabcfg'
EMAIL_FROM = 'zhengbigbig<780357902@qq.com>'
# 日志配置
# ADMINS = (('ZBB', '780357902@qq.com'),)
# 配置邮件
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SERVER_EMAIL = EMAIL_HOST_USER
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
#         }
#     },
#     'filters': {  # 过滤条件
#         # 要求debug是False才记录
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'logging.NullHandler',
#         },
#         'mail_admins': {  # 一旦线上代码报错，邮件提示
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#         },
#         'debug': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),  # 文件存储位置
#             'maxBytes': 1024 * 1024 * 5,  # 5M数据
#             'backupCount': 5,  # 允许5个这样的文件
#             'formatter': 'standard',  # 格式
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard',
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'django.request': {
#             'handlers': ['debug', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,  # 是否继承父类的log信息
#         },
#         # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
#         'django.security.DisallowedHost': {
#             'handlers': ['null'],
#             'propagate': False,
#         }
#     }
# }

