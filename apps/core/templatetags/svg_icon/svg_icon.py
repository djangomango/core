from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .helpers import load_path

register = template.Library()


@register.simple_tag
def svg_icon(
        icon_type,
        icon_name,
        view_box=24,
        size=20,
        fill_color='currentColor',
        fill_rule='evenodd',
        opacity=1,
        extra_class='',
        extra_style=''):
    icon_path = load_path(icon_type, icon_name)

    svg_tag = format_html(
        '<svg viewBox="0 0 {view_box} {view_box}" width="{size}" height="{size}" fill="{fill_color}" xmlns="http://www.w3.org/2000/svg"'
        'class="{extra_class}" style="{extra_style}" fill-rule="{fill_rule}" clip-rule="{fill_rule}">'
        '<path d="{path}" fill={fill_color} opacity={opacity}></path>'
        '</svg>',
        path=icon_path, view_box=view_box, size=size, fill_color=fill_color, fill_rule=fill_rule, opacity=opacity,
        extra_class=extra_class, extra_style=extra_style)

    return mark_safe(svg_tag)
