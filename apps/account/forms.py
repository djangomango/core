from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.core.fields.recaptcha import ReCaptchaField


class AuthenticationForm(DjangoAuthenticationForm):
    captcha = ReCaptchaField(score_threshold=0.5)

    remember = forms.BooleanField(
        label='Remember me',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
        )
        help_texts = {
            'username': _('Required. Please provide a valid username (3-30 characters).'),
            'password': _('Required. Please please provide your password.'),
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'autocomplete': 'username',
                'minlength': 3,
                'required': True
            }),
            'password': forms.PasswordInput(attrs={
                'autocomplete': 'current-password',
                'required': True
            }),
        }


class SetPasswordForm(DjangoSetPasswordForm):

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)

        if commit:
            self.user.save()

        self.user.pw_reset_on_login = False
        self.user.save()

        return self.user


class UserCreationForm(DjangoUserCreationForm):
    captcha = ReCaptchaField(
        score_threshold=0.5
    )

    password1 = forms.CharField(
        min_length=8,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
        }),
        help_text='Required. Please please provide a valid password (min 8 characters).',
        required=True
    )

    password2 = forms.CharField(
        min_length=8,
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text='Required. Enter the same password as above, for verification.',
        required=True
    )

    subscribe = forms.BooleanField(
        label='Subscribe to our newsletter',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email',)
        help_texts = {
            'first_name': _('Required. Please provide your first name (max 30 characters).'),
            'last_name': _('Required. Please provide your last name (max 30 characters).'),
            'username': _('Required. Please provide a valid username (3-30 characters).'),
            'email': _('Required. Please provide a valid email address (max 75 characters).'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'autocomplete': 'given-name',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'autocomplete': 'family-name',
                'required': True,
            }),
            'username': forms.TextInput(attrs={
                'autocomplete': 'username',
                'minlength': 3,
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email',
                'required': True,
            }),
        }


class CommonUserModelForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        help_texts = {
            'first_name': _('Required. Please provide your first name (max 30 characters).'),
            'last_name': _('Required. Please provide your last name (max 30 characters).'),
            'email': _('Required. Please provide a valid email address (max 75 characters).'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'autocomplete': 'given-name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'autocomplete': 'family-name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email',
                'required': True
            }),
        }
