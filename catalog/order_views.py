from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import OrderModelForm
from .mixins import PageTitleMixin
from .models import Order, OrderItem
from .loggers.query_logger_config import init_log
from .utils import consts
from .utils.main import query_log

active_tab_orders = '\'orders\''
log_name = consts.logs['order']
init_log(log_name)


class OrderListView(PageTitleMixin, LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10
    page_title = 'Ваши заказы'
    active_tab = active_tab_orders

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


@query_log(log_name=log_name)
@login_required
def order_confirm_delete_form(request, pk):
    page_title = 'Удалить заказ'
    order = Order.objects.get(order_id=pk)
    if request.method == 'POST':
        order_inst = Order.objects.get(order_id=pk)
        try:
            order_inst_items = OrderItem.objects.filter(
                order_id=pk)
            order_inst_items_count = len(order_inst_items)
        except ObjectDoesNotExist:
            order_inst_items_count = 0
        if order_inst_items_count:
            for item in order_inst_items:
                item.delete()

        order_inst.delete()

        return HttpResponseRedirect(reverse_lazy('orders'))
    else:
        form = OrderModelForm()

    return render(request, 'catalog/order_confirm_delete.html', {
            'form': form,
            'order': order,
            'page_title': page_title,
            'active_tab': active_tab_orders})
