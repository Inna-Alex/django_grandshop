from django.contrib import admin
from manufactor.models import Manufactor


@admin.register(Manufactor)
class ManufactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'created_date')
