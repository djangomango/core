from django import template
from django.utils.safestring import SafeString, mark_safe

from .helpers import render_icon

register = template.Library()


@register.simple_tag
def heroicon_outline(name, *, size=24, **kwargs):
    return _render_icon('outline', name, size, **kwargs)


@register.simple_tag
def heroicon_solid(name, *, size=24, **kwargs):
    return _render_icon('solid', name, size, **kwargs)


@register.simple_tag
def heroicon_mini(name, *, size=20, **kwargs):
    return _render_icon('mini', name, size, **kwargs)


def _render_icon(style, name, size=None, **kwargs):
    fixed_kwargs = {
        key: (value + "" if isinstance(value, SafeString) else value)
        for key, value in kwargs.items()
    }
    return mark_safe(render_icon(style, name, size, **fixed_kwargs))
