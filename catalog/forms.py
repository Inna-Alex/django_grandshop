from django import forms
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


class OrderItemUpdateModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemUpdateModelForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['orderitem'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = OrderItem
        fields = ['orderitem', 'quantity', 'price']
        labels = {'orderitem': _('Продукт'),
                  'quantity': _('Количество'),
                  'price': _('Цена, руб.')}


class CategoryRawModelForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'summary', 'availability']


class IssueForm(forms.Form):
    item_choices = []
    items = Item.objects.all()
    if items:
        for item in items:
            item_choices.append((item.item_id, item.name))

    select_item = forms.ChoiceField(
        widget=forms.Select,
        choices=item_choices,
        label='Продукт',
        required=True,
    )
    select_item.widget.attrs.update({'class': 'm-left-15'})


