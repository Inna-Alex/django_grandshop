from django import template
from django.template.defaultfilters import stringfilter

from catalog.utils.main import date_format_str

register = template.Library()


@register.filter
@stringfilter
def my_to_lower(value):
    return value.lower()


@register.filter
@stringfilter
def csv_bool_str(value):
    if value == 'В наличии':
        return value
    return 'Да' if value == 'True' else 'Нет'


@register.filter
@stringfilter
def csv_date_str(value):
    if value.startswith('Дата'):
        return value
    return date_format_str(value)
