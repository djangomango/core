from django.forms.widgets import Input


class ReCaptchaHiddenInput(Input):
    """
    Adapted from django-recaptcha3
    https://github.com/kbytesys/django-recaptcha3
    version 0.4.0
    """

    input_type = "hidden"
    template_name = "core/recaptcha/recaptcha_hidden_input.html"

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response', None)
