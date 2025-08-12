from django.urls import path
from .views import (sale_list_view, sale_cart_view,
                    sale_finalize_view, sale_item_delete,
                    sale_detail_view, payment_method_delete,
                    alter_sale_danger_view,)

urlpatterns = [
    path('list/', sale_list_view, name='sale_list'),
    path('list/<int:pk>/', sale_detail_view, name='sale_detail'),
    path('add/', sale_cart_view, name='start_sale'),
    path('finalize/', sale_finalize_view, name='sale_finalize'),
    path('item_delete/<int:pk>/', sale_item_delete, name='sale_item_delete'),
    path('payment_method_delete/<int:pk>/', payment_method_delete, name='payment_method_delete'),
    path('alter_sale_danger/<int:sale_id>/', alter_sale_danger_view, name='alter_sale_danger' ),
]
