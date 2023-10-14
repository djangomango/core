# Adapted from django-regex-field
# https://github.com/ambitioninc/django-regex-field
# version 3.0.3

import re

from django.core.exceptions import ValidationError
from django.db import models


class CastOnAssignDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class RegexField(models.CharField):
    description = "A regular expression"
    compiled_regex_cache = {}

    def __init__(self, *args, **kwargs):
        self.re_flags = kwargs.pop('re_flags', None)
        super(RegexField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = self.to_python(value)
        return self.value_to_string(value)

    def get_cache_key(self, value, flags):
        return 'value-{0}-flags-{1}'.format(value, flags)

    def get_compiled_regex(self, value):
        cache_key = self.get_cache_key(value, self.re_flags)
        if cache_key not in self.compiled_regex_cache:
            if self.re_flags is None:
                self.compiled_regex_cache[cache_key] = re.compile(value)
            else:
                self.compiled_regex_cache[cache_key] = re.compile(value, flags=self.re_flags)

        return self.compiled_regex_cache[cache_key]

    def from_db_value(self, value, expression, connection, *args):
        return self.to_python(value)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(RegexField, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, name, CastOnAssignDescriptor(self))

    def to_python(self, value):
        if isinstance(value, type(re.compile(''))):
            return value

        if value is None and self.null:
            return None

        try:
            return self.get_compiled_regex(value)
        except:
            raise ValidationError('Invalid regex {0}'.format(value))

    def value_to_string(self, obj):
        if obj is None:
            return None

        if issubclass(obj.__class__, models.Model):
            obj = self.value_from_object(obj)

        pattern_type = re.Pattern
        if isinstance(obj, pattern_type):
            return obj.pattern

        return None

    def run_validators(self, value):
        value = self.to_python(value)
        value = self.value_to_string(value)
        return super(RegexField, self).run_validators(value)
