# Adapted from django-recaptcha3
# https://github.com/kbytesys/django-recaptcha3
# version 0.4.0

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.helpers import get_google_recaptcha_config_or_none, get_google_recaptcha_response_or_none
from apps.core.widgets.recaptcha import ReCaptchaHiddenInput


class ReCaptchaField(forms.CharField):

    def __init__(self, attrs=None, *args, **kwargs):
        self._secret_key = kwargs.pop('recaptcha_config', None)
        self._score_threshold = kwargs.pop('score_threshold', None)

        if 'widget' not in kwargs:
            kwargs['widget'] = ReCaptchaHiddenInput()

        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        recaptcha_config = get_google_recaptcha_config_or_none()

        if not getattr(recaptcha_config, 'is_active', False):
            return None

        secret_key = self._secret_key or getattr(recaptcha_config, 'secret_key', None)
        score_threshold = self._score_threshold or getattr(recaptcha_config, 'threshold', 0.5)

        if not secret_key:
            raise ValidationError(
                _('reCaptcha not configured.'),
                code='invalid_config',
            )

        response_token = super(ReCaptchaField, self).clean(value)
        json_response = get_google_recaptcha_response_or_none(secret_key, response_token, threshold=score_threshold)

        if not json_response:
            raise ValidationError(
                _('reCaptcha response from Google not valid, try again.'),
                code='invalid_response',
            )

        if 'error-codes' in json_response:
            if 'missing-input-secret' in json_response['error-codes'] or \
                    'invalid-input-secret' in json_response['error-codes']:
                raise ValidationError(
                    _('Connection to reCaptcha server failed.'),
                    code='invalid_secret',
                )

            else:
                raise ValidationError(
                    _('reCaptcha invalid or expired, try again.'),
                    code='expired',
                )
