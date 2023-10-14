import json
import logging

from django import forms

from .config import Config
from .media import get_addon_media, get_mode_media, get_theme_media

logger = logging.getLogger('custom')


class CodeMirrorEditor(forms.Textarea):
    template_name = "core/codemirror/widget.html"

    def __init__(self, attrs=None, addons=[], **kwargs):
        self.config = Config()
        self.config.update(**kwargs)

        if addons:
            self.config.set_addons(addons)

        if not attrs:
            attrs = {}
        attrs['data-mirror'] = json.dumps(self.config.options)

        super().__init__(attrs)

    @property
    def media(self):
        media = forms.Media(
            css={
                # add: .CodeMirror { resize: vertical; overflow: hidden !important; } to allow resizing
                'all': ['codemirror/codemirror/lib/codemirror.css']
            },
            js=['codemirror/codemirror/lib/codemirror.js']
        )

        if 'mode' in self.config.options:
            try:
                media += get_mode_media(self.config.options['mode'])
            except ValueError as error:
                logger.error(str(error))

        if 'theme' in self.config.options:
            try:
                media += get_theme_media(self.config.options['theme'])
            except ValueError as error:
                logger.error(str(error))

        for addon in self.config.addons:
            try:
                media += get_addon_media(addon)
            except ValueError as error:
                logger.error(str(error))

        media += forms.Media(js=['codemirror/codemirror-init.js'])

        return media
