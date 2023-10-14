from django import forms

from apps.core.fields.recaptcha import ReCaptchaField


class CommonContactForm(forms.Form):
    captcha = ReCaptchaField(score_threshold=0.5)

    email = forms.EmailField(
        max_length=75,
        label='email',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
        }),
        help_text='Required. Please provide a valid email address (max 75 characters).',
        required=True
    )

class GeneralQueryForm(CommonContactForm):
    form_type = "general_query"

    first_name = forms.CharField(
        max_length=30,
        label='First name',
        widget=forms.TextInput(attrs={
            'autocomplete': 'given-name',
        }),
        help_text='Required. Please provide your first name (max 30 characters).',
        required=True
    )

    last_name = forms.CharField(
        max_length=30,
        label='Last name',
        widget=forms.TextInput(attrs={
            'autocomplete': 'family-name',
        }),
        help_text='Required. Please provide your last name (max 30 characters).',
        required=True
    )

    subject = forms.CharField(
        max_length=150,
        label='Subject',
        widget=forms.TextInput,
        help_text='Required. Please provide a subject.txt (max 150 characters).',
        required=True
    )

    message = forms.CharField(
        max_length=1500,
        label='Message',
        widget=forms.Textarea,
        help_text='Required. Please provide a message (max 1500 characters).',
        required=True
    )
