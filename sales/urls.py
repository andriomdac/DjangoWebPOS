from django.urls import path
from .views import sale_list_view, sale_cart_view, sale_finalize_view, sale_item_delete

urlpatterns = [
    path('list/', sale_list_view, name='sale_list'),
    path('add/', sale_cart_view, name='start_sale'),
    path('finalize/', sale_finalize_view, name='sale_finalize'),
    path('item_delete/<int:pk>/', sale_item_delete, name='sale_item_delete'),
]