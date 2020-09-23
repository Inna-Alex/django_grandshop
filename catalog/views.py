from django.shortcuts import render

from .basket_views import *
from .category_views import *
from .item_views import *
from .item_issue_views import *
from .manufactor_views import *
from .models import Category, Item, Manufactor
from .order_item_views import *
from .order_views import *


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
