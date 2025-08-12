from django.urls import path
from .views import webstore_home_view, webstore_cart_view

urlpatterns = [
    path('', webstore_home_view, name='webstore_home'),
    path('cart/', webstore_cart_view, name='webstore_cart'),
]