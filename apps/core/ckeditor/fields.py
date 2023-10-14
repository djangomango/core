import bleach
from django import forms
from django.db import models

from .widgets import CKEditorWidget

ALLOWED_TAGS = [
    'a', 'i', 'b', 'u', 'li', 'ol', 'ul', 'p', 'br', 'hr', 'strong', 'em',
]
ALLOWED_ATTRIBUTES = {}


def bleach_clean(html):
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True
    )


class RichTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop('config_name', 'default')
        self.extra_plugins = kwargs.pop('extra_plugins', [])
        self.external_plugin_resources = kwargs.pop('external_plugin_resources', [])
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RichTextFormField,
            'config_name': self.config_name,
            'extra_plugins': self.extra_plugins,
            'external_plugin_resources': self.external_plugin_resources,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class RichTextBleachedField(RichTextField):
    def __init__(self, *args, **kwargs):
        super(RichTextBleachedField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            value = bleach_clean(value)
        return value


class RichTextFormField(forms.CharField):
    widget = CKEditorWidget

    def __init__(
            self,
            config_name='default',
            extra_plugins=None,
            external_plugin_resources=None,
            *args,
            **kwargs
    ):
        kwargs['widget'] = self.widget(
            config_name=config_name,
            extra_plugins=extra_plugins,
            external_plugin_resources=external_plugin_resources,
        )
        super().__init__(*args, **kwargs)
