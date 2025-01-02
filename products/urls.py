from django.urls import path
from .views import (ProductCreateView, product_list_view,
                    ProductUpdateView, product_delete_view,
                    ProductDetailView, product_return_view,
                    product_return_list_view, product_item_add_to_sale,)

urlpatterns = [
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('list/', product_list_view, name='product_list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', product_delete_view, name='product_delete'),
    path('return/<int:pk>/', product_return_view, name='product_return'),
    path('return_list/', product_return_list_view, name='product_return_list'),
    path('product_item_add_to_sale/<int:pk>/', product_item_add_to_sale, name='product_item_add_to_sale')
]