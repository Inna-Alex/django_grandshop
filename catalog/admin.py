from django.contrib import admin

from .models import Category, Item, Manufactor, Order, OrderItem


@admin.register(Manufactor)
class ManufactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'created_date')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'availability', 'created_date')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'quantity',
                    'availability', 'created_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'comment', 'created_date')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'price', 'quantity', 'created_date')
