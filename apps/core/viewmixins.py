import logging

from django.views.generic.edit import View

from apps.core.forms import GeneralQueryForm
from apps.core.helpers import dispatch_email

logger = logging.getLogger('custom')


class CoreContactFormViewMixin(View):
    core_contact_forms = {
        'general_query': GeneralQueryForm,
    }

    core_contact_form_messages = {
        'general_query': 'Thank you for your query!',
    }

    def get_core_contact_form(self, form_type, data=None):
        user = self.request.user
        initial_data = {}
        if user.is_authenticated:
            initial_data = dict(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )

        return self.core_contact_forms[form_type](data, initial=initial_data)

    def post_core_contact_form_valid(self, form):
        form_type = form.form_type
        form_data = form.cleaned_data

        email = form_data.get('email', None)

        dispatch_email(email, form_type, form_data)
