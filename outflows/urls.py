from django.urls import path
from .views import outflow_create_view, OutflowListView

urlpatterns = [
    path('add/<int:pk>/', outflow_create_view, name='outflow_create'),
    path('list/', OutflowListView.as_view(), name='outflow_list'),]