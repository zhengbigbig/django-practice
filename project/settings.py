from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '=ij=9js^@-k)0bw!sd53zh8aeg$vm*46t#18bw0i+8fp2j+qux'

DEBUG = True

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
]
# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middleware.myApp.myMiddle.MyMiddle',
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

# celery
import djcelery

djcelery.setup_loader()  # 初始化
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_IMPORTS = ('myApp.task')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

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


# smtp邮箱服务
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '780357902@qq.com'
EMAIL_HOST_PASSWORD = '*******'
EMAIL_FROM = 'zhengbigbig<780357902@qq.com>'

# 黑名单设置
BLACKLIST = []