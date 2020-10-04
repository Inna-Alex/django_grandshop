from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import timesince
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from catalog.loggers.query_logger_config import init_log
from catalog.models import ru_time_strings
from catalog.utils import consts
from catalog.utils.main import query_log
from item.models import Item
from order.forms import OrderDetailModelForm, OrderItemCreateUpdateForm
from order.models import Order, OrderItem

active_tab = '\'orders\''
log_name = consts.logs['order_item']
init_log(log_name)


@query_log(log_name=log_name)
def orderitem_create_view(request, order_id):
    page_title = 'Добавить продукт в заказ'
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        form = OrderItemCreateUpdateForm(request.POST)
        if form.is_valid():
            order_inst = Order.objects.get(order_id=order_id)
            orderitem = OrderItem.objects.create(
                price=form.cleaned_data['price'],
                quantity=form.cleaned_data['quantity'],
                order=order_inst,
                orderitem=form.cleaned_data['orderitem'])
            orderitem.save()
            return HttpResponseRedirect(reverse('order_detail',
                                                kwargs={'pk': order_id}))

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        form = OrderItemCreateUpdateForm(initial={'order': order_id, 'quantity': 1})

    return render(
        request,
        'order/orderitem_form.html',
        context={'form': form, 'order_id': order_id, 'page_title': page_title, 'active_tab': active_tab}
    )


@query_log(log_name=log_name)
def orderitem_update_view(request, pk):
    page_title = 'Редактировать продукт заказа'
    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        quantity = request.POST.get('quantity', None)
        price = request.POST.get('price', None)
        order_item = OrderItem.objects.get(order_item_id=pk)

        form = OrderItemCreateUpdateForm(initial={
            'order': order_id,
            'pk': pk,
            'orderitem': order_item.orderitem.item_id,
            'quantity': quantity,
            'price': price})

        return render(
            request,
            'order/orderitem_update.html',
            context={'form': form,
                     'order_id': order_id,
                     'order_item_id': pk,
                     'orderitem': order_item.orderitem,
                     'quantity': quantity,
                     'price': price,
                     'page_title': page_title,
                     'active_tab': active_tab}
        )


@query_log(log_name=log_name)
def orderitem_update_save_view(request, pk):
    if request.method == 'POST':
        form = OrderItemCreateUpdateForm(request.POST)
        if form.is_valid():
            orderitem = OrderItem.objects.get(order_item_id=pk)
            orderitem.quantity = form.cleaned_data['quantity']
            orderitem.price = form.cleaned_data['price']
            orderitem.save()

            return HttpResponseRedirect(reverse(
                'order_detail',
                kwargs={'pk': orderitem.order_id}))
        else:
            order_item = OrderItem.objects.get(order_item_id=pk)

            return render(
                request,
                'order/orderitem_update.html',
                context={'form': form,
                         'order_item_id': pk,
                         'orderitem': order_item.orderitem,
                         'active_tab': active_tab}
            )


@query_log(log_name=log_name)
def calculate_price(request, orderitem=None):
    quantity = request.GET.get('quantity', None)
    if orderitem is None:
        orderitem = request.GET.get('orderitem', None)

    item = Item.objects.get(item_id=orderitem)
    to_pay = item.price * int(quantity)
    data = {
        'to_pay': to_pay
    }
    return JsonResponse(data)


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('orders')


@query_log(log_name=log_name)
def show_order_detail_view(request, pk):
    page_title = 'Заказ'
    order_items = OrderItem.objects.filter(order_id=pk).select_related('order')
    if order_items:
        order = order_items.first().order
    else:
        order = Order.objects.get(order_id=pk)
    form = OrderDetailModelForm()
    since_time = "{} назад".format(timesince(order.created_date, time_strings=ru_time_strings))

    if request.method == 'POST':
        form = OrderDetailModelForm(data=request.POST)
        if form.is_valid():
            form.save()
        else:
            form = OrderDetailModelForm()

    return render(request, 'order/order_detail.html', {
            'form': form,
            'order': order,
            'sincetime': since_time,
            'order_items': order_items,
            'page_title': page_title,
            'active_tab': active_tab})


@query_log(log_name=log_name)
def remove_order_detail_items_view(request):
    page_title = 'Заказ'
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        order_id = request.POST.get('order_id')
        order_item = OrderItem.objects.select_related('order').get(order_item_id=order_item_id)
        order = order_item.order
        order_item.delete()

        form = OrderDetailModelForm()
        order_items = OrderItem.objects.filter(order_id=order_id)
        return render(request, 'order/order_detail.html', {
            'form': form,
            'order': order,
            'order_items': order_items,
            'page_title': page_title,
            'active_tab': active_tab})
