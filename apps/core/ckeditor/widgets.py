from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.widgets import Media
from django.templatetags.static import static
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.translation import get_language

from apps.core.tags import JS
from .settings import DEFAULT_CONFIG, CKEDITOR_CONFIGS


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


json_encode = LazyEncoder().encode


class CKEditorWidget(forms.Textarea):
    template_name = "core/ckeditor/base-widget.html"

    def __init__(
            self,
            config_name='default',
            extra_plugins=None,
            external_plugin_resources=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.config_name = config_name
        self.config = DEFAULT_CONFIG.copy()

        configs = CKEDITOR_CONFIGS
        if configs:
            if isinstance(configs, dict):
                if self.config_name in configs:
                    config = configs[self.config_name]
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured(
                            'CKEDITOR_CONFIGS["%s"] \
                                setting must be a dictionary type.'
                            % self.config_name
                        )
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured(
                        "No configuration named '%s' \
                            found in your CKEDITOR_CONFIGS setting."
                        % self.config_name
                    )
            else:
                raise ImproperlyConfigured(
                    "CKEDITOR_CONFIGS setting must be a\
                        dictionary type."
                )

        extra_plugins = extra_plugins or self.config.pop('extra_plugins', None) or []

        if extra_plugins:
            self.config['extraPlugins'] = ",".join(extra_plugins)

        self.external_plugin_resources = (
                external_plugin_resources
                or self.config.pop('external_plugin_resources', None)
                or []
        )

    @property
    def media(self):
        return Media(
            js=(
                JS(
                    'ckeditor/ckeditor-init.js',
                    {
                        'id': 'ckeditor-init-script',
                        'data-ckeditor-basepath': static('ckeditor/ckeditor/'),
                    },
                ),
                'ckeditor/ckeditor/ckeditor.js',
            )
        )

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        self._set_config()
        context['widget']['config'] = json_encode(self.config)

        external_plugin_resources = [
            [force_str(a), force_str(b), force_str(c)]
            for a, b, c in self.external_plugin_resources
        ]
        context['widget']['external_plugin_resources'] = json_encode(
            external_plugin_resources
        )
        return context

    def _set_config(self):
        lang = get_language().lower()
        if lang == "zh-hans":
            lang = "zh-cn"
        elif lang == "zh-hant":
            lang = "zh"
        self.config['language'] = lang


class CKEditorTailwindWidget(CKEditorWidget):
    template_name = "core/ckeditor/tailwind-widget.html"
