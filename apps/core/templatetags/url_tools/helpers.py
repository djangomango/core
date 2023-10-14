import urllib.parse

from django.http.request import QueryDict
from django.utils.encoding import iri_to_uri


def del_dict_item_if_exists(dic, key):
    try:
        del dic[key]
    except KeyError:
        pass


class UrlHelper(object):
    """
    Helper class for manipulating URLs.

    Attributes:
        path (str): The path component of the URL.
        fragment (str): The fragment identifier component of the URL.
        query_dict (QueryDict): A dictionary-like object representing the query parameters of the URL.

    Methods:
        get_query_string(**kwargs): Returns the query string representation of the current query parameters.
        update_query_data(**kwargs): Updates the current query parameters with the given key-value pairs.
        get_full_path(**kwargs): Returns the full URL with the query parameters updated according to the given key-value pairs.
        overload_params(**kwargs): Overloads the current query parameters with the given key-value pairs.
        del_params(*params, **kwargs): Deletes the given query parameters from the current query string.
        toggle_params(**params): Toggles the given query parameters in the current query string.

    Usage:
        url_helper = UrlHelper(request.get_full_path())
        url_helper.update_query_data(page=2)
        url_helper.toggle_params(tag='django', author='jane')
        updated_url = str(url_helper)
    """

    def __init__(self, full_path):
        if type(full_path) is UrlHelper:
            full_path = full_path.get_full_path()

        r = urllib.parse.urlparse(full_path)

        self.path = r.path
        self.fragment = r.fragment
        self.query_dict = QueryDict(r.query, mutable=True)

    def get_query_string(self, **kwargs):
        return self.query_dict.urlencode(**kwargs)

    def update_query_data(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(val, '__iter__'):
                self.query_dict.setlist(key, val)
            else:
                self.query_dict[key] = val

    def get_full_path(self, **kwargs):
        query_string = self.get_query_string(**kwargs)
        if query_string:
            query_string = '?%s' % query_string

        fragment = self.fragment and '#%s' % iri_to_uri(self.fragment) or ''

        return '%s%s%s' % (
            iri_to_uri(self.path),
            query_string,
            fragment
        )

    def overload_params(self, **kwargs):
        for key, val in kwargs.items():
            uniques = set(self.query_dict.getlist(key))
            uniques.add(val)
            self.query_dict.setlist(key, list(uniques))

    def del_params(self, *params, **kwargs):
        if not params and not kwargs:
            self.query = {}
            return

        if params:
            for param in params:
                del_dict_item_if_exists(self.query_dict, param)

        if kwargs:
            for key, val in kwargs.items():
                to_keep = [
                    x for x in self.query_dict.getlist(key)
                    if not x.startswith(val)
                ]
                self.query_dict.setlist(key, to_keep)

    def toggle_params(self, **params):
        for param, value in params.items():
            value = value.decode('utf-8')
            if value in self.query_dict.getlist(param):
                self.del_params(**{param: value})
            else:
                self.overload_params(**{param: value})

    def __str__(self):
        return self.get_full_path()
