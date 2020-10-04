from django import forms
from item.models import Item


def get_item_choices():
    return [(item.item_id, item.name) for item in Item.objects.all()]


class IssueForm(forms.Form):
    select_item = forms.ChoiceField(
        widget=forms.Select,
        choices=get_item_choices,
        label='Продукт',
        required=True,
    )
    select_item.widget.attrs.update({'class': 'm-left-15'})
