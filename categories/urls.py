from django.urls import path
from .views import category_add_view, category_list_view

urlpatterns = [
    path('add/', category_add_view, name='category_create'),
    path('list/', category_list_view, name='category_list'),

]