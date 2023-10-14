import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

logger = logging.getLogger('custom')


@require_GET
def robots_txt(request):
    lines = [
        'User-Agent: *',
        'Disallow: /admin/',
        'Disallow: /membership/',
    ]

    return HttpResponse('\n'.join(lines), content_type='text/plain')


def maintenance(request):
    return render(request, 'maintenance.html')
