from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Category


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10


# CRUD
class CategoryDetailView(generic.DetailView):
    model = Category


class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'summary', 'availability']


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
