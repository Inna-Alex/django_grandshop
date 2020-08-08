from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Item

active_tab = '\'items\''


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


# CRUD
class ItemDetailView(generic.DetailView):
    model = Item
    
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ItemCreateView(CreateView):
    model = Item
    fields = ['manufactor', 'category', 'name', 'summary', 'price',
              'availability', 'quantity']

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['name', 'summary', 'availability', 'price', 'quantity']

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('items')

    def get_context_data(self, **kwargs):
        context = super(ItemDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context
