import re

from django.core.exceptions import MiddlewareNotUsed
from django.shortcuts import redirect
from django.urls import reverse

from apps.account.helpers import is_user_active_staff
from apps.core.helpers import get_maintenance_mode_or_false


class MaintenanceModeMiddleware:
    allowed_patterns = [
        r'^/admin/',
        r'^/static/',
        r'^/account/login/$',
        r'^/maintenance/$',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

        if not get_maintenance_mode_or_false():
            raise MiddlewareNotUsed

    def __call__(self, request):
        if not is_user_active_staff(request.user):

            match = False
            for pattern in self.allowed_patterns:

                if re.compile(pattern).match(request.path):
                    match = True
                    break

            if not match:
                return redirect(reverse('maintenance'))

        return self.get_response(request)
