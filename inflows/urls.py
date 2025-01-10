from django.urls import path
from .views import inflow_create_view, InflowListView, InflowDetailView

urlpatterns = [
    path('add/<int:pk>/', inflow_create_view, name='inflow_create'),
    path('list/', InflowListView.as_view(), name='inflow_list'),
    path('list/<int:pk>/', InflowDetailView.as_view(), name='inflow_detail')
]
