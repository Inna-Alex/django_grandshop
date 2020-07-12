from django.shortcuts import render
from django.views import generic

from .models import Manufactor, Category, Item, Order, OrderItem
from .order_views import *
from .order_item_views import *
from .manufactor_views import *
from .category_views import *
from .item_views import *

def index(request):
    """
    Ф-ция отображения домашней страницы
    """
    num_manufactors = Manufactor.objects.all().count()
    num_categories = Category.objects.all().count()
    num_items = Item.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_manufactors':num_manufactors,
                 'num_categories':num_categories,
                 'num_items':num_items,}
    )

