from apps.core.helpers import get_site_config_or_none


def base(request):
    ctx = {
        'base_url': request.build_absolute_uri('/').rstrip('/'),
        'full_url': request.build_absolute_uri,
    }

    return ctx


def site_config(request):
    ctx = {}

    site_config = get_site_config_or_none()
    if site_config:
        ctx.update({
            'site_config': site_config,
            'navigation_link': site_config.navigation_link.all(),
            'config_google_recaptcha': site_config.config_google_recaptcha,
        })

    return ctx
