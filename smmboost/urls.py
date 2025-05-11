from django.urls import path
from . import views

app_name = 'smmboost'

urlpatterns = [
    path('refill/<int:order_id>/', views.request_refill, name='request_refill'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),

    path('fetch-services/', views.fetch_services, name='fetch_services'),
    path('services/', views.service_list, name='services'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('check-status/<int:order_id>/', views.check_status, name='check_status'),
]
