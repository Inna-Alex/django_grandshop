from django.contrib import admin

from .models import Category, Item, Manufactor, Order, OrderItem


@admin.register(Manufactor)
class ManufactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'availability')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'quantity', 'availability')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'comment')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'price', 'quantity')
