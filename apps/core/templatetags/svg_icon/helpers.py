import functools
import os
from contextlib import closing
from zipfile import ZipFile

icon_zip_paths = {
    'material': 'data/material_icons.zip',  # https://github.com/livingdocsIO/material-design-icons-svg
    'custom': 'data/custom_icons.zip',
}


class IconDoesNotExist(Exception):
    pass


@functools.lru_cache(maxsize=128)
def load_path(icon_type, icon_name):
    path = None

    icon_zip_path = icon_zip_paths.get(icon_type, None)
    icon_zip_path = os.path.join(os.path.dirname(__file__), icon_zip_path)
    if icon_zip_path:
        if os.path.exists(icon_zip_path):
            f = open(icon_zip_path, 'rb')
            with closing(ZipFile(f, 'r')) as zip_file:
                try:
                    zf = zip_file.open(f"{icon_name}.json")
                    path = zf.read().decode('utf-8').strip('"')
                except IconDoesNotExist:
                    pass

    return path
