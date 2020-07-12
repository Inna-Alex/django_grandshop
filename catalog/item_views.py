from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Item

class ItemListView(generic.ListView):
    model = Item
    paginate_by = 10

""" CRUD """
class ItemDetailView(generic.DetailView):
    model = Item

class ItemCreate(CreateView):
    model = Item
    fields = ['manufactor','category','name','summary','price','availability',
              'quantity',]
    #labels = { 'manufactor': _('Производитель'),
     #          'name': _('Название'), }

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name','summary','availability','price','quantity']

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('items')
""" CRUD """
