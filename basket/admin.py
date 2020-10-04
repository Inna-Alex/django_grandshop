from django.contrib import admin

from basket.models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('basket_id', 'item', 'quantity', 'customer', 'created_date')
