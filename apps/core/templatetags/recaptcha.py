# Adapted from django-recaptcha3
# https://github.com/kbytesys/django-recaptcha3
# version 0.4.0

from django import template
from django.template.loader import get_template

from apps.core.helpers import get_google_recaptcha_config_or_none

register = template.Library()


@register.simple_tag
def recaptcha_key():
    recaptcha_config = get_google_recaptcha_config_or_none()
    return getattr(recaptcha_config, 'site_key', None)


@register.inclusion_tag(get_template('core/recaptcha/recaptcha_init.html'))
def recaptcha_init():
    return {
        'public_key': recaptcha_key(),
    }


@register.inclusion_tag(get_template('core/recaptcha/recaptcha_ready.html'))
def recaptcha_ready(action_name=None):
    return {
        'public_key': recaptcha_key(),
        'action_name': action_name or 'generic',
    }


@register.inclusion_tag(get_template('core/recaptcha/recaptcha_execute.html'))
def recaptcha_execute(action_name=None):
    return {
        'public_key': recaptcha_key(),
        'action_name': action_name or 'generic',
    }
