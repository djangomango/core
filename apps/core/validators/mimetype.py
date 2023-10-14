import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MimeTypeValidator(object):

    def __init__(self, mimetypes, message=None, code='file-type'):
        self.mimetypes = mimetypes
        self.message = message
        self.code = code

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(2048), mime=True)
        except magic.MagicException:
            raise ValidationError('Value could not be validated for file type %s.' % value, code='file-type')

        if mime != 'application/octet-stream' and not mime in self.mimetypes:
            if not self.message:
                raise ValidationError(_('%s is not an acceptable file type.') % value, code=self.code)
            else:
                raise ValidationError(_(self.message), code=self.code)
