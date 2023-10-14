from .common import *

# APP DEFINITION
# ------------------------------------------------------------------------------

GZIP_COMPRESSION_ENABLED = os.getenv('DJANGO_GZIP_COMPRESSION_ENABLED', True) == "True"
if GZIP_COMPRESSION_ENABLED:
    MIDDLEWARE = [
                     'django.middleware.gzip.GZipMiddleware',
                 ] + MIDDLEWARE

REDIS_CACHE_ENABLED = os.getenv('DJANGO_REDIS_CACHE_ENABLED', True) == "True"
if REDIS_CACHE_ENABLED:
    MIDDLEWARE = [
                     'django.middleware.cache.UpdateCacheMiddleware',
                 ] + MIDDLEWARE

    MIDDLEWARE += [
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://redis:6379',
        },
    }

    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_KEY_PREFIX = ""
    CACHE_MIDDLEWARE_SECONDS = 600

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

cached_loaders = (
    'django.template.loaders.cached.Loader',
    [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ],
)

for options in TEMPLATES:
    options['OPTIONS']['loaders'] = [
        cached_loaders,
    ]

# WEBPACK LOADER
# ------------------------------------------------------------------------------

WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(BASE_DIR, 'frontend', 'webpack-stats.prod.json')

# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
# http://www.django-rest-framework.org/

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
