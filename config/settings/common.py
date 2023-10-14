import json
import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

# SECRET KEY
# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# DEBUG
# ------------------------------------------------------------------------------
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv('DJANGO_DEBUG', False) == "True"
DEBUG_TOOLBAR = os.getenv('DJANGO_DEBUG_TOOLBAR', False) == "True"

# ALLOWED HOSTS
# ------------------------------------------------------------------------------

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1').split(',')

# SSL
# ------------------------------------------------------------------------------

SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', False) == "True"

if os.getenv('DJANGO_SECURE_PROXY_SSL_HEADER_CHECK', False) == "True":
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

ADMINS = (
    ('Admin', ADMIN_EMAIL),
)

MANAGERS = ADMINS

# APP CONFIGURATION
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.forms',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'solo',
    'webpack_loader',
]

LOCAL_APPS = [
    'apps.account.apps.AccountConfig',
    'apps.attachment.apps.AttachmentConfig',
    'apps.core.apps.CoreConfig',
    'apps.log.apps.LogConfig',
    'apps.page.apps.PageConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# SITES
# ------------------------------------------------------------------------------

SITE_ID = 1

DJANGO_SITE_NAME = os.getenv('DJANGO_SITE_NAME', 'Django')
DJANGO_SITE_DOMAIN = os.getenv('DJANGO_SITE_DOMAIN', 'django.com')

# AUTH USER
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = "account.User"

# LOGIN REDIRECT
# ------------------------------------------------------------------------------

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_REDIRECT_URL = "/"

# MIDDLEWARE
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.maintenancemode.MaintenanceModeMiddleware',
    'apps.core.middleware.authrequired.AuthRequiredMiddleware'
]

HTML_MINIFY_ENABLED = os.getenv('DJANGO_HTML_MINIFY_ENABLED', False) == "True"
if HTML_MINIFY_ENABLED:
    MIDDLEWARE = [
                     'apps.core.middleware.htmlminify.HTMLMinifyMiddleware',
                 ] + MIDDLEWARE

VISIT_LOG_ENABLED = os.getenv('DJANGO_VISIT_LOG_ENABLED', False) == "True"
if VISIT_LOG_ENABLED:
    MIDDLEWARE += [
        'apps.log.middleware.VisitLogMiddleware',
    ]

# ROOT URL CONFIGURATION
# ------------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.base',
                'apps.core.context_processors.site_config',
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# WGSI CONFIGURATION
# ------------------------------------------------------------------------------

WSGI_APPLICATION = "config.wsgi.application"

# X-FRAME OPTIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/clickjacking/#setting-x-frame-options-for-all-responses

X_FRAME_OPTIONS = "SAMEORIGIN"

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': json.loads(
            os.getenv('DB_OPTIONS', '{}')
        ),
    }
}

# DEFAULT AUTO FIELD
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# SESSIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#sessions

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/topics/email/

DEFAULT_FROM_EMAIL = os.getenv('ADMIN_EMAIL')

SMTP_EMAIL = os.getenv('SMTP_EMAIL', False) == "True"
if SMTP_EMAIL:
    EMAIL_BACKEND = "apps.core.backends.SmtpEmailLogBackend"
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True) == "True"
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False) == "True"
else:
    EMAIL_BACKEND = "apps.core.backends.ConsoleEmailLogBackend"

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STORAGES
# ------------------------------------------------------------------------------

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'private': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# AWS

AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')

AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_DOMAIN_NAME = os.getenv('AWS_S3_DOMAIN_NAME')
AWS_S3_ENDPOINT_URL = "https://{}.{}.{}".format(AWS_S3_BUCKET_NAME, AWS_S3_REGION_NAME, AWS_S3_DOMAIN_NAME)

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = "public-read"

# Azure

AZURE_BLOB_ACCOUNT_NAME = os.getenv('AZURE_BLOB_ACCOUNT_NAME')
AZURE_BLOB_ACCOUNT_KEY = os.getenv('AZURE_BLOB_ACCOUNT_KEY')

AZURE_BLOB_CONTAINER_NAME = os.getenv('AZURE_BLOB_CONTAINER_NAME')
AZURE_BLOB_CUSTOM_DOMAIN = os.getenv('AZURE_BLOB_CUSTOM_DOMAIN')
AZURE_BLOB_ENDPOINT_URL = "https://{}".format(AZURE_BLOB_CUSTOM_DOMAIN)

# STATIC FILES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# MEDIA FILES
# ------------------------------------------------------------------------------

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# AWS

AWS_MEDIA_STORAGE = os.getenv('AWS_MEDIA_STORAGE', False) == "True"
if AWS_MEDIA_STORAGE:
    INSTALLED_APPS += [
        'storages',
    ]

    STORAGES['default']['BACKEND'] = "config.storages.S3BotoPublicMediaStorage"
    STORAGES['private']['BACKEND'] = "config.storages.S3BotoPrivateMediaStorage"

    AWS_S3_MEDIA_ROOT = "media"

    MEDIA_URL = "{}/{}/{}/".format(AWS_S3_ENDPOINT_URL, AWS_S3_BUCKET_NAME, AWS_S3_MEDIA_ROOT)
    MEDIA_ROOT = MEDIA_URL

# Azure

AZURE_MEDIA_STORAGE = os.getenv('AZURE_MEDIA_STORAGE', False) == "True"
if AZURE_MEDIA_STORAGE:
    INSTALLED_APPS += [
        'storages',
    ]

    STORAGES['default']['BACKEND'] = "config.storages.AzurePublicMediaStorage"
    STORAGES['private']['BACKEND'] = "config.storages.AzurePrivateMediaStorage"

    AZURE_BLOB_MEDIA_ROOT = "media"

    MEDIA_URL = "{}/{}/".format(AZURE_BLOB_ENDPOINT_URL, AZURE_BLOB_MEDIA_ROOT)
    MEDIA_ROOT = MEDIA_URL

# CELERY
# ------------------------------------------------------------------------------
# https://github.com/celery/django-celery-beat

CELERY_BROKER_URL = os.getenv('DJANGO_CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('DJANGO_CELERY_RESULT_BACKEND')
CELERY_BEAT_SCHEDULER = os.getenv('DJANGO_CELERY_BEAT_SCHEDULER')

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE

# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SIMPLE JWT
# ------------------------------------------------------------------------------
# https://github.com/jazzband/djangorestframework-simplejwt

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# GOOGLE RECAPTCHA
# ------------------------------------------------------------------------------
# https://www.google.com/recaptcha/about/

GOOGLE_RECAPTCHA_IS_ACTIVE = os.getenv('GOOGLE_RECAPTCHA_IS_ACTIVE', False) == "True"
GOOGLE_RECAPTCHA_SITE_KEY = os.getenv('GOOGLE_RECAPTCHA_SITE_KEY')
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('GOOGLE_RECAPTCHA_SECRET_KEY')
GOOGLE_RECAPTCHA_SCORE_THRESHOLD = os.getenv('GOOGLE_RECAPTCHA_SCORE_THRESHOLD')

# MAILCHIMP
# ------------------------------------------------------------------------------
# https://mailchimp.com/

MAILCHIMP_IS_ACTIVE = os.getenv('MAILCHIMP_IS_ACTIVE', False) == "True"
MAILCHIMP_KEY = os.getenv('MAILCHIMP_KEY')

# WEBPACK LOADER
# ------------------------------------------------------------------------------
# https://github.com/django-webpack/django-webpack-loader

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'build/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.dev.json'),
        'POLL_INTERVAL': 0.1,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    },
}

# DJANGO COUNTRIES
# ------------------------------------------------------------------------------
# https://github.com/SmileyChris/django-countries/

COUNTRIES_FIRST = ['US', 'GB']

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.2/topics/logging/

LOGGING_CONFIG = None

import logging.config
from ..logger import LOGGING

logging.config.dictConfig(LOGGING)

# SENTRY
# ------------------------------------------------------------------------------
# https://sentry.io/for/django/

SENTRY_ENABLED = os.getenv('SENTRY_ENABLED', False) == "True"
if SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN' ''),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        release=os.environ.get('SENTRY_RELEASE', '1.0.0')
    )

# OTHER
# ------------------------------------------------------------------------------

SESSION_COOKIE_AGE = int(os.getenv('DJANGO_SESSION_COOKIE_AGE', default=60 * 60 * 24 * 30))
MAX_UPLOAD_SIZE = int(os.getenv('DJANGO_MAX_UPLOAD_SIZE', default=4 * 1024 * 1024))
