import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordChangeDoneView as DjangoPasswordChangeDoneView
from django.contrib.auth.views import PasswordResetCompleteView as DjangoPasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView as DjangoPasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.http.response import JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.account.forms import AuthenticationForm, SetPasswordForm
from apps.account.forms import UserCreationForm
from apps.core.viewmixins import dispatch_email

logger = logging.getLogger('custom')


class LoginView(DjangoLoginView):
    template_name = "account/login.html"
    success_url = reverse_lazy('portal:index')
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == "XMLHttpRequest":
            login_form = self.form_class(data=request.POST)

            if login_form.is_valid():
                return self.get_response_post_form_valid(request, login_form)

            if '__all__' in login_form.errors.keys():
                return JsonResponse({'status': 500, 'message': {'error': login_form.non_field_errors()[0]}})

            return JsonResponse({'status': 500, 'message': login_form.errors})

        ctx = super(LoginView, self).get_context_data(**kwargs)

        return render(request, self.template_name, ctx)

    def get_context_data(self, **kwargs):
        ctx = super(LoginView, self).get_context_data(**kwargs)
        ctx['login_form'] = self.form_class(data=self.request.POST or None)

        return ctx

    def get_response_post_form_valid(self, request, form):
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        remember = form.cleaned_data.get('remember', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if user.pw_reset_on_login:
                return JsonResponse({'status': 200, 'url': reverse('account:password_reset')})

            login(request, user)

            if remember:
                request.session.set_expiry(0)

            return JsonResponse({'status': 200, 'url': self.success_url})

        return JsonResponse({'status': 500, 'message': 'Authentication error'})


class RegisterFormView(FormView):
    template_name = 'account/register.html'
    success_url = reverse_lazy('portal:index')
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == "XMLHttpRequest":
            register_form = self.form_class(request.POST or None)
            if register_form.is_valid():
                return self.post_form_valid(request, register_form)

            return JsonResponse({'status': 500, 'message': {**register_form.errors}})

        ctx = super(RegisterFormView, self).get_context_data(**kwargs)

        return render(request, self.template_name, ctx)

    def get_context_data(self, **kwargs):
        ctx = super(RegisterFormView, self).get_context_data(**kwargs)
        ctx['register_form'] = self.form_class(
            self.request.POST or None,
            instance=self.request.user if self.request.user.is_authenticated else None
        )

        return ctx

    def post_form_valid(self, request, form):
        user = form.save()
        user.activate()

        user = authenticate(
            request,
            username=user.username,
            password=form.cleaned_data.get('password1')
        )

        if user:
            login(request, user)

        subscribe = form.cleaned_data.pop('subscribe', False)
        if subscribe:
            user.add_newsletter_sub()

        email_type = "register_account_request"
        email_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        dispatch_email(user.email, email_type, email_data)

        return JsonResponse({'status': 200, 'url': self.success_url})


class PasswordResetView(DjangoPasswordResetView):
    template_name = "account/password/reset-form.html"
    email_template_name = "common/account/password/reset-email.html"
    subject_template_name = "common/account/password/reset-subject.txt"
    success_url = reverse_lazy('account:password_reset_done')


class PasswordChangeDoneView(DjangoPasswordChangeDoneView):
    template_name = "account/password/reset-form.html"
    email_template_name = "common/account/password/reset-email.html"
    subject_template_name = "common/account/password/reset-subject.txt"
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = "account/password/reset-done.html"


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = "account/password/reset-confirm.html"
    success_url = reverse_lazy('account:password_reset_complete')
    form_class = SetPasswordForm


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = "account/password/reset-complete.html"
