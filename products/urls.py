from django.urls import path
from .views import (ProductCreateView, ProductListView,
                    ProductUpdateView, product_delete_view,
                    ProductDetailView, product_return_view)

urlpatterns = [
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('list/', ProductListView.as_view(), name='product_list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', product_delete_view, name='product_delete'),
    path('return/<int:pk>/', product_return_view, name='product_return'),
]