from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import OrderItem, Order

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
        fields = ['orderitem','quantity', 'price']
        labels = { 'orderitem': _('Продукт'),
                   'quantity': _('Количество'),
                   'price': _('Цена, руб.') }
        initial={'quantity':'1'}


class OrderItemUpdateModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(OrderItemUpdateModelForm, self).__init__(*args, **kwargs)
       self.fields['price'].widget.attrs['readonly'] = True
       self.fields['orderitem'].widget.attrs['disabled'] = 'disabled'
       
    class Meta:
        model = OrderItem
        fields = ['orderitem','quantity', 'price']
        labels = { 'orderitem': _('Продукт'),
                   'quantity': _('Количество'),
                   'price': _('Цена, руб.') }

