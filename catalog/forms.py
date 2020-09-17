from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Category, Item, Order, OrderItem


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['comment']


class OrderDetailModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'comment', 'customer']


class OrderItemCreateModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True

    class Meta:
        model = OrderItem
        fields = ['orderitem', 'quantity', 'price']
        labels = {'orderitem': _('Продукт'),
                  'quantity': _('Количество'),
                  'price': _('Цена, руб.')}
        initial = {'quantity': '1'}

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise ValidationError(_('Поле Количество должно быть > 0'), code='invalid')
        return quantity


class OrderItemUpdateModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemUpdateModelForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True
        # self.fields['orderitem'].widget.attrs['disabled'] = 'disabled'

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


