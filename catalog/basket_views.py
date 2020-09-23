from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic.base import RedirectView

from .models import Basket, Item, Order, OrderItem
from .mixins import PageTitleMixin
from .loggers.query_logger_config import init_log
from .utils import consts
from .utils.main import query_log

active_tab = '\'orders\''
log_name = consts.logs['basket']
init_log(log_name)


class BasketListView(PageTitleMixin, LoginRequiredMixin, generic.ListView):
    model = Basket
    paginate_by = 10
    page_title = 'Корзина'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def get_context_data(self, **kwargs):
        context = super(BasketListView, self).get_context_data(**kwargs)
        total = sum((basket.item.price for basket in self.get_queryset()))
        context['total'] = total
        return context

    def get_queryset(self):
        return Basket.objects.filter(customer=self.request.user).select_related('item')


class AddItemToBasketRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'item_detail'

    @query_log(log_name=log_name)
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        item = Item.objects.get(item_id=kwargs['pk'])
        if item:
            Basket.objects.create(item=item, customer=user)

        return super(AddItemToBasketRedirectView, self).get_redirect_url(*args, **kwargs)


@query_log(log_name=log_name)
def rm_item_from_basket_view(request, pk):
    if request.method == 'POST':
        try:
            basket_item = Basket.objects.select_related('item').get(basket_id=pk)
            if basket_item:
                basket_item.delete()
        except ObjectDoesNotExist:
            pass

        return redirect(reverse('basket'))


class CreateOrderFromBasketRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'order_detail'

    @query_log(log_name=log_name)
    def get_redirect_url(self, *args, **kwargs):
        baskets = Basket.objects.select_related('item').filter(customer=self.request.user)
        order = Order.objects.create(customer=self.request.user)
        for basket in baskets:
            OrderItem.objects.create(order=order, orderitem=basket.item,
                                     quantity=basket.quantity, price=basket.item.price*basket.quantity)
            basket.delete()
        kwargs['pk'] = order.order_id

        return super(CreateOrderFromBasketRedirectView, self).get_redirect_url(*args, **kwargs)
