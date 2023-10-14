import re

from django import template
from django.template import Node
from django.utils.encoding import force_str

register = template.Library()


def strip_spaces_in_tags(value):
    value = force_str(value)
    value = re.sub(r'\s+', ' ', value)
    value = re.sub(r'>\s+', '>', value)
    value = re.sub(r'\s+<', '<', value)
    return value


class NoSpacesNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_spaces_in_tags(self.nodelist.render(context).strip())


@register.tag
def all_spaceless(parser, token):
    nodelist = parser.parse(('end_all_spaceless',))
    parser.delete_first_token()
    return NoSpacesNode(nodelist)
