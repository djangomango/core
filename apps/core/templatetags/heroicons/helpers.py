import os
import functools
from contextlib import closing
from copy import deepcopy
from xml.etree import ElementTree
from zipfile import ZipFile


class IconDoesNotExist(Exception):
    pass


@functools.lru_cache(maxsize=128)
def _load_icon(icon_style, icon_name):
    path = os.path.join(os.path.dirname(__file__), 'data/heroicons.zip')
    if path:
        f = open(path, 'rb')
        with closing(ZipFile(f, 'r')) as zip_file:
            try:
                svg_bytes = zip_file.read(f"{icon_style}/{icon_name}.svg")
            except KeyError:
                raise IconDoesNotExist(
                    f"The icon {icon_name!r} with style {icon_style!r} does not exist."
                )

            svg = ElementTree.fromstring(svg_bytes.decode())
            for node in svg.iter():
                node.tag = ElementTree.QName(
                    str.removeprefix(node.tag, '{http://www.w3.org/2000/svg}')
                )
            return svg


_PATH_ATTR_NAMES = frozenset(
    {
        'stroke-linecap',
        'stroke-linejoin',
        'vector-effect',
    }
)


def render_icon(icon_style, icon_name, icon_size, **kwargs):
    svg = deepcopy(_load_icon(icon_style, icon_name))
    if icon_size is not None:
        svg.attrib['width'] = svg.attrib['height'] = str(icon_size)

    svg_attrs = {}
    path_attrs = {}
    for raw_name, value in kwargs.items():
        icon_name = raw_name.replace('_', '-')
        if icon_name in _PATH_ATTR_NAMES:
            path_attrs[icon_name] = str(value)
        else:
            svg_attrs[icon_name] = str(value)

    svg.attrib.update(svg_attrs)
    if path_attrs:
        for path in svg.findall('path'):
            path.attrib.update(path_attrs)

    string = ElementTree.tostring(svg, encoding='unicode')
    return string.replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
