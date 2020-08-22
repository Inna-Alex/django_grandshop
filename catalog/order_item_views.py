from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import timesince
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView

from .forms import OrderDetailModelForm
from .forms import OrderItemCreateModelForm, OrderItemUpdateModelForm
from .models import Item, Order, OrderItem, ru_time_strings

active_tab = '\'orders\''


class OrderItemListView(generic.ListView):
    model = OrderItem
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrderItemListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class OrderItemDetailView(generic.DetailView):
    model = OrderItem


def orderitem_create_view(request, order_id):
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса
        # (связывание, binding):
        form = OrderItemCreateModelForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
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
        form = OrderItemCreateModelForm(initial={'order': order_id})

    return render(
        request,
        'catalog/orderitem_form.html',
        context={'form': form, 'order_id': order_id,
                 'active_tab': active_tab}
    )


def orderitem_update_view(request, pk):
    order_id = request.POST.get('order_id', None)
    quantity = request.POST.get('quantity', None)
    price = request.POST.get('price', None)
    order_item = OrderItem.objects.get(order_item_id=pk)

    form = OrderItemUpdateModelForm(initial={
        'order': order_id,
        'pk': pk,
        'orderitem': order_item.orderitem.item_id,
        'quantity': quantity,
        'price': price})

    return render(
        request,
        'catalog/orderitem_update.html',
        context={'form': form,
                 'order_id': order_id,
                 'order_item_id': pk,
                 'orderitem': order_item.orderitem.item_id,
                 'quantity': quantity,
                 'price': price,
                 'active_tab': active_tab}
    )


def orderitem_update_save_view(request, pk):
    if request.method == 'POST':
        form = OrderItemUpdateModelForm(request.POST)
        if form.is_valid():
            orderitem = OrderItem.objects.get(order_item_id=pk)
            orderitem.quantity = form.cleaned_data['quantity']
            orderitem.price = form.cleaned_data['price']
            orderitem.save()
            return HttpResponseRedirect(reverse(
                'order_detail',
                kwargs={'pk': orderitem.order_id}))


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


def show_order_detail_view(request, pk):
    order = Order.objects.get(order_id=pk)
    order_items = OrderItem.objects.filter(order_id__exact=pk)
    form = OrderDetailModelForm()
    since_time = "{} назад".format(timesince(order.created_date, time_strings=ru_time_strings))

    if request.method == 'POST':
        form = OrderDetailModelForm(data=request.POST)
        if form.is_valid():
            form.save()
        else:
            form = OrderDetailModelForm()

    return render(request, 'catalog/order_detail.html', {
            'form': form,
            'order': order,
            'sincetime': since_time,
            'order_items': order_items,
            'active_tab': active_tab})


def remove_order_detail_items_view(request):
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        order_id = request.POST.get('order_id')
        order_item = OrderItem.objects.get(order_item_id=order_item_id)
        order_item.delete()

        form = OrderDetailModelForm()
        order = Order.objects.get(order_id=order_id)
        order_items = OrderItem.objects.filter(order_id__exact=order_id)
        return render(request, 'catalog/order_detail.html', {
            'form': form,
            'order': order,
            'order_items': order_items,
            'active_tab': active_tab})
