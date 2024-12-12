from django.urls import path
from .views import BrandCreateView, BrandListView, BrandUpdateView, brand_delete_view, BrandDetailView

urlpatterns = [
    path('add/', BrandCreateView.as_view(), name='brand_create'),
    path('list/', BrandListView.as_view(), name='brand_list'),
    path('list/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('delete/<int:pk>', brand_delete_view, name='brand_delete'),
]