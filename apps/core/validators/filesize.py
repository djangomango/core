from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator(object):

    def __init__(self, size):
        self.size = size

    def __call__(self, value):
        img_mb = round(value.size / 1048576, 1)
        max_mb = round(self.size / 1048576, 1)

        if value.size > self.size:
            raise ValidationError(_('File size must be less than %s mb. Your file is %s mb.') % (max_mb, img_mb),
                                  code='file-size')
