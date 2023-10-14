from django.apps import apps
from django.contrib import admin

from apps.core.models import ConfigGoogleRecaptcha
from apps.utils.mixins.admin.core import AutoModelAdminMixin, AutoModelNoModuleAdminMixin

app_config = apps.get_app_config('core')

app_config.model_imports()

no_module_models = (
    ConfigGoogleRecaptcha,
)

models = app_config.get_models()
for model in models:
    try:
        if model in no_module_models:
            admin.site.register(model, AutoModelNoModuleAdminMixin)
        else:
            admin.site.register(model, AutoModelAdminMixin)

    except admin.sites.AlreadyRegistered:
        pass
