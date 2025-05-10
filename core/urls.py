from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('message/<slug:celeb>/', views.send_message_to_celeb, name='send_message_to_celeb'),

    path('<slug:slug>/', views.celebrity_profile, name='celebrity_profile'),
    path('<slug:slug>/register/', views.fan_registration, name='fan_registration'),
]
