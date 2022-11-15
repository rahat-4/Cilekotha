from django.urls import path
from . import views

app_name = 'App_Order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name="cart"),
    path('cart/', views.view_cart, name="view_cart"),
    path('remove/<pk>/', views.remove_from_cart, name="remove"),
    path('increase-quantity/<pk>/', views.increase_quantity, name="increase_quantity"),
    path('decrease-quantity/<pk>/', views.decrease_quanity, name="decrease_quantity"),
]