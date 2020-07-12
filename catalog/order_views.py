from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, OrderItem
from .forms import OrderModelForm, OrderDetailModelForm

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['comment']
    initial={'status':'c'}

class OrderUpdate(UpdateView):
    model = Order
    fields = ['comment','status']

def order_confirm_delete_form(request, pk):
    order = Order.objects.get(order_id=pk)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        order_inst = Order.objects.get(order_id=pk)
        try:
            order_inst_items = OrderItem.objects.filter(order_id__exact=order_inst.order_id)
            order_inst_items_count = len(order_inst_items)
        except ObjectDoesNotExist:
            order_inst_items_count = 0
        if order_inst_items_count:
            for item in order_inst_items:
                item.delete()
                
        order_inst.delete()
        
        return HttpResponseRedirect(reverse_lazy('orders') )
    else:
        form = OrderModelForm()
        
    return render(request, 'catalog/order_confirm_delete.html', {
            'form': form,
            'order': order} )
        
            




        
