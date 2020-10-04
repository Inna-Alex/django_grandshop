from django.forms import ModelForm

from .models import Category


class CategoryRawModelForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'summary', 'availability']
