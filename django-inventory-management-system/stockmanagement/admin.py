from django.contrib import admin

from .models import *
from .forms import *


class StockCreateAdmin(admin.ModelAdmin):
    list_display = [

        'category',
        'item_name',
        'quantity'
    ]

    form = StockCreateForm

    list_filter = ['category']

    search_fields = [

        'category',
        'item_name'
    ]


class OrderCheckAdmin(admin.ModelAdmin):
    list_display = [

        'issue_to',
        'item_name',
        'quantity'
    ]

    form = StockCreateForm

    list_filter = ['item_name']

    search_fields = [

        'issue_to',
        'item_name'
    ]


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(StockHistory, OrderCheckAdmin)
# admin.site.register(Category)
