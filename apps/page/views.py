import logging

from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.viewmixins import CoreContactFormViewMixin
from apps.page.models import LandingPage

logger = logging.getLogger('custom')


class LandingPageTemplateView(CoreContactFormViewMixin, TemplateView):
    template_name = "page/landing/index.html"

    def post(self, request, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)

        return render(request, self.template_name, ctx)

    def get_context_data(self, **kwargs):
        ctx = super(LandingPageTemplateView, self).get_context_data(**kwargs)

        landing_page = LandingPage.get_solo()

        ctx['landing_page'] = landing_page

        return ctx
