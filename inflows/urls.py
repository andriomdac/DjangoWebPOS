from django.urls import path
from .views import inflow_create_view, InflowListView

urlpatterns = [
    path('add/<int:pk>/', inflow_create_view, name='inflow_create'),
    path('list/', InflowListView.as_view(), name='inflow_list'),]