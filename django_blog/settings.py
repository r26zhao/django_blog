"""
Django settings for django_blog project.
Generated by 'django-admin startproject' using Django 1.11.2.
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8q@q!u=s#vgqz7=s)2au6w4ae@4mt8i=#76x6ll-x_jbs-_zh%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.aaron-zhao.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.weibo',
    'crispy_forms',
    'imagekit',
    'robots',
    'mptt',
    'easy_comment',
    'notifications',
    'online_status',
    'django_celery_results',
]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'online_status.middleware.OnlineStatusMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.views.global_setting',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogdb',
        'USER': 'root',
        "PASSWORD": 'mangui710',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# Media root 设置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 富文本编辑器设置

CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'language':'zh-cn',
        'width': '750px',
        'height': '500px',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote',
                       '-','JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor', '-', 'RemoveFormat']},
            {'name': 'insert',
             'items': ['Image', '-', 'Flash', 'Iframe', '-', 'Table', 'CodeSnippet', 'Templates']},
            '/',
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'special', 'items': ['Subscript', 'Superscript', '-', 'HorizontalRule',
                                          'SpecialChar', 'Smiley']},
            {'name': 'tools', 'items': ['Undo', 'Redo', '-', 'Source', 'Preview', 'Save', '-', 'Maximize']}
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'image_previewText':' ',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath',
                'codesnippet',
                'uploadimage',
                'uploadfile',
                'prism',
            ]),
    },
    'comment': {
        # 编辑器的宽高请根据你的页面自行设置
        'width': 'auto',
        'height': '150px',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['CodeSnippet'],
            ['Image', 'Link', 'Unlink']
        ],
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'prism', 'widget', 'lineutils', ]),
    }

}
# 自定义日志输出信息
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters':['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            },
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'log/all.log',     #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'log/error.log',
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            },
        'console':{
            'level': 'INFO',
            'filters':['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            },
        'scripts_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'scripts': {
            'handlers': ['scripts_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'blog.views': {
            'handlers': ['default', 'error', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

# Website INFO  Global Var
SITE_NAME = 'Python学习笔记、Django学习笔记 - AA的博客'
SITE_DESCP = 'AA的博客是分享学习Python技术与经验的个人博客，由Python、Django以及资源分享等分类组成，内容主要是Django博客开发。'
SITE_KEYWORDS = 'AA的博客, Python学习笔记, Django博客开发, Django学习笔记'

# 自定义用户model
AUTH_USER_MODEL = 'blog.user'

# django-allauth相关设置
AUTHENTICATION_BACKENDS = (
# django admin所使用的用户登录与django-allauth无关
    'django.contrib.auth.backends.ModelBackend',

# `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 前面我们app里添加了django.contrib.sites,需要设置SITE_ID
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_LOGOUT_ON_GET = True

# Email setting
# SMTP服务器，我使用的是sendclound的服务
EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_HOST_USER = 'support@aaron-zhao.com'
EMAIL_HOST_PASSWORD = '1234'
EMAIL_PORT = 465
#EMAIL_HOST = 'smtpcloud.sohu.com'
#EMAIL_HOST_USER = 'Aaroon_test_N05MI9'  'bguqzpoxqlhccaig' qq
#EMAIL_HOST_PASSWORD = 'u7qFYbkRKK08PMtR'
#EMAIL_PORT = 25
# 是否使用了SSL 或者TLS
EMAIL_USE_SSL = True
#EMAIL_USE_TLS = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = 'Support <support@aaron-zhao.com>'
ADMINS = (('Aaron', 'rudy710@qq.com'), ('Barry', 'zhruyao@163.com'))
#非空链接，却发生404错误，发送通知MANAGERS
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

# easy_comment setting
COMMENT_ENTRY_MODEL = 'blog.post'
ROBOTS_USE_HOST = False

# notification setting
NOTIFICATIONS_USE_JSONFIELD=True
SEND_NOTIFICATION_EMAIL = True

#redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

#celery settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-cache'
