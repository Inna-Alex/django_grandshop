from django.contrib import admin

from item_issue.models import ItemIssue


@admin.register(ItemIssue)
class ItemIssueAdmin(admin.ModelAdmin):
    list_display = ('item_issue_id', 'item', 'created_by', 'created_date')
