import logging

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.models import SiteConfig
from apps.utils.helpers.requests import get_request_parsed_ua_string

logger = logging.getLogger('custom')


def get_site_config_or_none():
    return SiteConfig.objects.filter(is_active=True).last()


def get_maintenance_mode_or_false():
    site_config = get_site_config_or_none()
    return getattr(site_config, 'maintenance_mode', False)


def get_auth_required_or_false():
    site_config = get_site_config_or_none()
    return getattr(site_config, 'auth_required', False)


def get_google_recaptcha_config_or_none():
    site_config = get_site_config_or_none()
    return getattr(site_config, 'config_google_recaptcha', None)


def get_google_recaptcha_response_or_none(secret_key, recaptcha_response, threshold=None):
    data = {
        'secret': secret_key,
        'response': recaptcha_response
    }

    response = None

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', timeout=5, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(e)

    json_response = response.json()
    if bool(json_response.get('success', False)):
        if threshold:
            if json_response.get('score') > threshold:
                return json_response

    return None


def dispatch_email(email, email_type, email_data):
    site_config = get_site_config_or_none()
    if site_config:
        email_data.update({
            'site_name': site_config.site.name,
            'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
            'domain': site_config.site.domain,
            'admin_email': settings.ADMIN_EMAIL,
            'social_link': site_config.social_link.all().values('type', 'social_url')
        })

        tpl_dir = f"core/emails/{email_type}"
        subject_tpl = "subject.txt"
        body_text_tpl = "body.txt"
        body_html_tpl = "body.html"

        subject = render_to_string(f'{tpl_dir}/{subject_tpl}', email_data)
        body_text = render_to_string(f'{tpl_dir}/{body_text_tpl}', email_data)
        body_html = render_to_string(f'{tpl_dir}/{body_html_tpl}', email_data)

        email = EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=settings.ADMIN_EMAIL,
            to=[email],
            bcc=[settings.ADMIN_EMAIL]
        )

        email.attach_alternative(body_html, 'text/html')

        email.send()


def check_request_ua_supported(request):
    unsupported_agents = [
        {'family': 'IE', 'major': 11},
        {'family': 'Edge', 'major': 17},
        {'family': 'Firefox', 'major': 64},
        {'family': 'Chrome', 'major': 8},
        {'family': 'Safari', 'major': 13.1},
        {'family': 'Opera', 'major': 10.1},
        {'family': 'Mobile Safari', 'major': 13.7},
    ]

    parsed_agent = get_request_parsed_ua_string(request, parse='agent')
    agent_family = parsed_agent.get('family', '')
    agent_major = parsed_agent.get('major', 0)

    result = True
    for agent in unsupported_agents:

        if agent_family == agent['family']:

            try:
                if float(agent_major) <= agent['major']:
                    result = False
            except ValueError as e:
                logging.error(e)

    return result
