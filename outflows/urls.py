from django.urls import path
from .views import outflow_create_view, outflow_list_view, OutflowDetailView

urlpatterns = [
    path('add/<int:pk>/', outflow_create_view, name='outflow_create'),
    path('list/', outflow_list_view, name='outflow_list'),
    path('list/<int:pk>/', OutflowDetailView.as_view(), name='outflow_detail'),
]
