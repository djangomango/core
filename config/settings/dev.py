from .common import *

INTERNAL_IPS = ['127.0.0.1']

# APP DEFINITION
# ------------------------------------------------------------------------------

if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar'
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

default_loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

for options in TEMPLATES:
    options['OPTIONS']['loaders'] = default_loaders

# OTHER
# ------------------------------------------------------------------------------

DATA_UPLOAD_MAX_NUMBER_FIELDS = None
