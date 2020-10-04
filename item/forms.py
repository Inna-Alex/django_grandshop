from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from item.models import Item


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
