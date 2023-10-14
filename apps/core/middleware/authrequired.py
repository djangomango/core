import re

from django.core.exceptions import MiddlewareNotUsed
from django.shortcuts import redirect
from django.urls import reverse

from apps.core.helpers import get_auth_required_or_false


class AuthRequiredMiddleware:
    allowed_patterns = [
        r'^/admin/',
        r'^/static/',
        r'^/account/login/$',
        r'^/account/password-reset/$',
        r'^/account/password-reset-done/$',
        r'^/account/password-reset-complete/$',
        r'^/account/password-change-done/$',
        r'^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,36})/$',
        r'^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/set-password/$'
        r'^/maintenance/$',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

        if not get_auth_required_or_false():
            raise MiddlewareNotUsed

    def __call__(self, request):
        if not request.user.is_authenticated:

            match = False
            for pattern in self.allowed_patterns:

                if re.compile(pattern).match(request.path):
                    match = True
                    break

            if not match:
                return redirect(reverse('account:login'))

        return self.get_response(request)
