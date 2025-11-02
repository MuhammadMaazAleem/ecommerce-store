from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create/', views.create_order, name='create_order'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
]
