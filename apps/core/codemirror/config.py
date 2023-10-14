from django.core.exceptions import ImproperlyConfigured

from apps.utils.helpers.string import snake_to_camel
from .settings import DJANGO_MIRROR_DEFAULTS


class Config:
    """
    A config instance represents a CodeMirror configuration [1]. Usage:
        config = Config()
        config.update(read_only=True, addons=['dialog/dialog'])
        assert config.options == {'readOnly': True}
        assert config.addons == ['dialog/dialog.js']
    [1]: https://codemirror.net/doc/manual.html#config
    """

    def __init__(self):
        self.options = {}
        self.addons = []

        try:
            self.update(**DJANGO_MIRROR_DEFAULTS)
        except TypeError:
            message = 'DJANGO_MIRROR_DEFAULTS should be a dict.'
            raise ImproperlyConfigured(message)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'addons':
                self.set_addons(value)
            else:
                self.options[snake_to_camel(key)] = value

    def set_addons(self, addons):
        self.addons = [
            addon if addon.endswith('.js') else addon + '.js'
            for addon in addons
        ]
