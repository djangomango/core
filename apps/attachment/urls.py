from django.urls import path

from apps.attachment import views

app_name = "attachment"

urlpatterns = [

    path('file/<uuid:uuid>/', views.file_attachment, name='file'),
    path('image/<uuid:uuid>/', views.image_attachment, name='image'),

]
