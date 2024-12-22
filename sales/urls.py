from django.urls import path
from .views import SaleListView, sale_view, sale_finalize_view

urlpatterns = [
    path('list/', SaleListView.as_view(), name='sale_list'),
    path('add/', sale_view, name='start_sale'),
    path('finalize/', sale_finalize_view, name='sale_finalize')
]