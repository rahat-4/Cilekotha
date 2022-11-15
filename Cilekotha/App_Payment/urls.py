from django.urls import path
from . import views

app_name = 'App_Payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('status/', views.status, name='status'),
    path('payment-status', views.payment_status, name='payment_status'),
    path('purchased/<val_id>/<tran_id>/', views.purchased_order, name='purchased_order'),
    path('order/', views.order_view, name='order_view')
]