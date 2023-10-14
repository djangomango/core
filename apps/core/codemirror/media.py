import json
import os.path

from django.forms.widgets import Media

from .settings import CODEMIRROR_DIR

MEDIA_PATHS = {}
with open(os.path.join(os.path.dirname(__file__), 'media.json')) as f:
    MEDIA_PATHS = json.load(f)


def _follow(path):
    reqs = []
    if path in MEDIA_PATHS:
        for another in MEDIA_PATHS[path]:
            reqs += _follow(another)
    return reqs + [path]


def _make(path):
    css, js = [], []

    for req in _follow(path):
        req = os.path.join('codemirror/codemirror', req)

        if req.endswith('.css'):
            css.append(req)
        elif req.endswith('.js'):
            js.append(req)

    return Media(css={'all': css}, js=js)


def get_mode_media(mode):
    path = 'mode/{}/{}.js'.format(mode, mode)

    if path not in MEDIA_PATHS:
        raise ValueError('Unknown mode: {!s}'.format(mode))

    return _make(path)


def get_addon_media(addon):
    path = 'addon/{}'.format(addon if addon.endswith('.js') else addon + '.js')

    if path not in MEDIA_PATHS:
        raise ValueError('Unknown addon: {!s}'.format(addon))

    return _make(path)


def get_theme_media(theme):
    path = 'theme/{}.css'.format(theme)

    if not os.path.exists(os.path.join(CODEMIRROR_DIR, path)):
        raise ValueError('Unknown theme: {!s}'.format(theme))

    return Media(css={'all': [path]})
