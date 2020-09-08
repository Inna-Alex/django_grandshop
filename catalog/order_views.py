import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from catalog.loggers.query_logger import QueryLogger
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts
from .forms import OrderModelForm
from .models import Order, OrderItem

active_tab_orders = '\'orders\''
active_tab_order_create = '\'order_create\''
log_name = consts.logs['order']
init_log(log_name)
logger = logging.getLogger(log_name)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            context = super(OrderListView, self).get_context_data(**kwargs)
            context['active_tab'] = active_tab_orders
        logger.info(str(ql))

        return context

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['comment']
    initial = {'status': 'c'}

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab_order_create
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(OrderCreateView, self).form_valid(form)
        logger.info(str(ql))

        return response


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['comment', 'status']

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab_orders
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(OrderUpdateView, self).form_valid(form)
        logger.info(str(ql))

        return response


def order_confirm_delete_form(request, pk):
    ql = QueryLogger()
    with connection.execute_wrapper(ql):
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
    logger.info(str(ql))

    return render(request, 'catalog/order_confirm_delete.html', {
            'form': form,
            'order': order,
            'active_tab': active_tab_orders})
