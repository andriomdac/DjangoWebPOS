from django.urls import path
from .views import order_detail_view, orders_list_view, deactivate_order, accept_order, finished_orders_list_view

urlpatterns = [
    path('list/', orders_list_view, name='orders_list'),
    path('detail/<int:order_id>/', order_detail_view, name='order_detail'),
    path('finished_orders/', finished_orders_list_view, name='finished_orders_list'),

    path('deactivate_order/<int:order_id>/', deactivate_order, name='deactivate_order'),
    path('accept_order/<int:order_id>/', accept_order, name='accept_order'),

]