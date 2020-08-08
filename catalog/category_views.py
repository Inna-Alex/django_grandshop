from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Category

active_tab = '\'categories\''


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


# CRUD
class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'summary', 'availability']

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context
