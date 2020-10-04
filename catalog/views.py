from django.shortcuts import render

from category.models import Category
from item.models import Item
from manufactor.models import Manufactor


def index(request):
    """
    Ф-ция отображения домашней страницы
    """
    num_manufactors = Manufactor.objects.all().count()
    num_categories = Category.objects.all().count()
    num_items = Item.objects.all().count()
    page_title = 'Главная'
    active_tab = '\'index\''

    return render(
        request,
        'index.html',
        context={'num_manufactors': num_manufactors,
                 'num_categories': num_categories,
                 'num_items': num_items,
                 'page_title': page_title,
                 'active_tab': active_tab}
    )
