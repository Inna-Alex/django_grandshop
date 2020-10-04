from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from order.models import Order, OrderItem


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
