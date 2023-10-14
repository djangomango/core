from django.contrib.auth import views as auth_views
from django.urls import path

from apps.account import views

app_name = "account"

urlpatterns = [

    path('register/', views.RegisterFormView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
