from django.urls import path
from .views import (CategoryCreateView, CategoryListView,
                    CategoryUpdateView, category_delete_view,
                    CategoryDetailView)

urlpatterns = [
    path('add/', CategoryCreateView.as_view(), name='category_create'),
    path('list/', CategoryListView.as_view(), name='category_list'),
    path('list/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('delete/<int:pk>', category_delete_view, name='category_delete'),
]
