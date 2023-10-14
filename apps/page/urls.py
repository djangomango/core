from django.urls import path

from apps.page import views

app_name = "page"

urlpatterns = [

    path('', views.LandingPageTemplateView.as_view(), name='index'),

]
