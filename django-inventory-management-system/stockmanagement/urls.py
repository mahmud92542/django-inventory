from django.contrib import admin
from django.urls import path

from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('add_items', add_items, name='add_items'),
    path('list_items', list_items, name='list_items'),
    path('update_items/<str:pk>/', update_items, name="update_items"),
    #path('delete_items/<str:pk>/', delete_items, name="delete_items"),
    path('stock_detail/<str:pk>/', stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>/', issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', reorder_level, name="reorder_level"),
    path('order_history/', order_history, name='order_history'),
]
