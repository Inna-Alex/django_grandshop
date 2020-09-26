from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Basket, Category, Item, Order, OrderItem


class ItemCreateUpdateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['manufactor', 'category', 'name', 'summary', 'availability', 'price', 'quantity']

    def clean_manufactor(self):
        manufactor = self.cleaned_data.get('manufactor')
        if manufactor is None:
            raise ValidationError(_('Поле Производитель не должно быть пустым'), code='invalid')
        return manufactor

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is None:
            raise ValidationError(_('Поле Категория не должно быть пустым'), code='invalid')
        return category

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError(_('Цена должна быть > 0'), code='invalid')
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise ValidationError(_('Количество должно быть >= 0'), code='invalid')
        return quantity


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class OrderDetailModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'customer']


class OrderItemCreateUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True

    class Meta:
        model = OrderItem
        fields = ['orderitem', 'quantity', 'price']
        labels = {'orderitem': _('Продукт'),
                  'quantity': _('Количество'),
                  'price': _('Цена, руб.')}

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise ValidationError(_('Поле Количество должно быть > 0'), code='invalid')
        return quantity


class CategoryRawModelForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'summary', 'availability']


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
