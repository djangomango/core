import decimal
import re
from datetime import date, datetime

import requests
from django import template
from django.core.files.storage import default_storage
from django.db import models

from apps.utils.helpers.requests import get_agent_head_or_default

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict) and isinstance(key, (int, str, float, bool)):
        return dictionary.get(key)

    return dictionary


@register.filter
def starts_with(string, starts):
    if isinstance(string, str) and isinstance(starts, str):
        return string.startswith(starts)

    return string


@register.filter
def ends_with(string, ends):
    if isinstance(string, str) and isinstance(ends, str):
        return string.endswith(ends)

    return string


@register.filter
def remove_substr(string, substr):
    if isinstance(string, str) and isinstance(substr, str):
        string = string.replace(substr, '')

    return string


@register.simple_tag
def replace_substr(string, substr, newstr):
    if all(isinstance(i, str) for i in [string, substr, newstr]):
        string = string.replace(substr, newstr)

    return string


@register.filter
def short_email(string):
    if isinstance(string, str):
        if '@' in string:
            string = string[string.index('@'):]

    return string


@register.filter
def short_url(string):
    if isinstance(string, str):
        if string.startswith('http'):
            string = re.sub(r'https?://', '', string)
        if string.startswith('www.'):
            string = re.sub(r'www.', '', string)
        if string.endswith('/'):
            string = string[:-1]

    return string


@register.filter
def short_number(value):
    if isinstance(value, (int, float, decimal.Decimal)):
        value_int = int(value)
        if value_int > 1000000:
            value = "%.0f%s" % (value_int / 1000000, 'M')
        elif value_int > 1000:
            value = "%.0f%s" % (value_int / 1000, 'k')

    return value


@register.filter(expects_localtime=True)
def days_since(dt):
    if isinstance(dt, date):
        tzinfo = getattr(dt, 'tzinfo', None)
        day = date(dt.year, dt.month, dt.day)
        today = datetime.now(tzinfo).date()
        delta = day - today
        return abs(delta.days)

    return dt


@register.filter
def divide(value, divisor):
    if all(isinstance(i, (int, float, decimal.Decimal)) for i in [value, divisor]):
        return float(value) / float(divisor)

    return value


@register.filter
def file_exists(file):
    if isinstance(file, models.FileField):
        return default_storage.exists(file.path)

    return False


@register.filter
def url_exists(url):
    if isinstance(url, str):
        head = get_agent_head_or_default()
        req = requests.get(url, headers=head, timeout=2)
        return req.status_code == requests.codes.ok

    return False
