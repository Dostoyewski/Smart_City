"""
Django settings for Smart_City project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import mimetypes

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(7o=r7ij92do@da1p6*8xq#p-*&m+lx*hw0kc0hc$q^hrs4%)a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

if DEBUG:
    ALLOWED_HOSTS = ['*']

# allauth params:
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

# mailing params:
ACCOUNT_ACTIVATION_DAYS = 2
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nik.tesla637@gmail.com'
EMAIL_HOST_PASSWORD = 'Tesla123!'
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'main',
    'telemetry',
    'webpush',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vk',
    'imagekit',
    'ckeditor',
    'ckeditor_uploader',
    'colorful',
    'adminsortable',
    'djeym',
    'yandex_maps',
    'map'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Smart_City.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'Smart_City.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '',
            'secret': '',
            'key': ''
        }
    }
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BGE1WfBYo8v-o3ots4dK2zLyJo2M8V64rdcNrJsB4Zjx2Mjo5GMB9C-fGFr-XeBCWk23gBZ6WUevGAxSd1LcF8U",
    "VAPID_PRIVATE_KEY": "MXCNkC9v2PRDHiV-EPCwHtCC1IIyNmzbvy_8yhmjmGc",
    "VAPID_ADMIN_EMAIL": "fdrkondor@gmail.com"
}

NOTIFICATION_KEY = 'BPIag9NQTlil0FLram4-5zZdQ6a0bcl6yzL3h0zUAewCpli1Jz9av0tcQsyLSAjuXeqAsYaRDnYRKaVcheBMCIg'
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = "/static"
mimetypes.add_type("application/javascript", STATIC_ROOT + "/js/.js", True)

# To send test messages.
# 1. Notify administrator of a new custom marker.
# 2. Notify user about successful moderation of his marker.
# Mail server for testings: $ python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@site.net'

# django-ckeditor
# https://github.com/django-ckeditor/django-ckeditor
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'djeym.utils.get_filename'
CKEDITOR_THUMBNAIL_SIZE = (300, 300)
CKEDITOR_FORCE_JPEG_COMPRESSION = True
CKEDITOR_IMAGE_QUALITY = 40
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False  # False - Only image files. (At your discretion)
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
    },
    'djeym': {
        'toolbar': 'full',
        'height': 400,
        'width': 362,
        'colorButton_colors': 'F44336,C62828,E91E63,AD1457,9C27B0,6A1B9A,'
                              '673AB7,4527A0,3F51B5,283593,2196F3,1565C0,'
                              '03A9F4,0277BD,00BCD4,00838F,009688,00695C,'
                              '4CAF50,2E7D32,8BC34A,558B2F,CDDC39,9E9D24,'
                              'FFEB3B,F9A825,FFC107,FF8F00,FF9800,EF6C00,'
                              'FF5722,D84315,795548,4E342E,607D8B,37474F,'
                              '9E9E9E,424242,000000,FFFFFF',
        'colorButton_enableAutomatic': False,
        'colorButton_enableMore': True
    }
}


PROJECT_ROOT = BASE_DIR

# Settings specific for koalixcrm


# Settings specific for filebrowser


# (If a non-authenticated user requests an editor page.)
# (Если не аутентифицированный пользователь запросит страницу редактора.)
LOGIN_URL = '/admin/'  # or change to your URL

# Required for django-admin-sortable
# https://github.com/alsoicode/django-admin-sortable#configuration
CSRF_COOKIE_HTTPONLY = False

# The API key is used in the free and paid versions.
# You can get the key in the developer’s office - https://passport.yandex.com/
# ( API-ключ используется в свободной и платной версиях.
#   Получить ключ можно в кабинете разработчика - https://developer.tech.yandex.ru/ )
DJEYM_YMAPS_API_KEY = 'fafde453-2c72-4d6e-b318-fda89f6c09ef'
YANDEX_MAPS_API_KEY = 'fafde453-2c72-4d6e-b318-fda89f6c09ef'

# For paid use API --> True
# ( Для платного использования --> True )
DJEYM_YMAPS_API_KEY_FOR_ENTERPRISE = False

# Map download mode. Default = 'release'
# (Режим загрузки карт.)
# DJEYM_YMAPS_DOWNLOAD_MODE = 'debug'
