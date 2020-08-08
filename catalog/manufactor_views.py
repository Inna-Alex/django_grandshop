from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Manufactor

active_tab = '\'manufactors\''


class ManufactorListView(generic.ListView):
    model = Manufactor
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ManufactorListView, self).get_context_data(**kwargs)
        context['great_manufactor_name'] = 'ASUS manufactor'
        context['great_manufactor_summary'] = 'Summary for ASUS manufactor'
        context['active_tab'] = active_tab
        return context


# CRUD
class ManufactorDetailView(generic.DetailView):
    model = Manufactor

    def get_context_data(self, **kwargs):
        context = super(ManufactorDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ManufactorCreateView(CreateView):
    model = Manufactor
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ManufactorCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ManufactorUpdateView(UpdateView):
    model = Manufactor
    fields = ['name', 'summary']

    def get_context_data(self, **kwargs):
        context = super(ManufactorUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context


class ManufactorDeleteView(DeleteView):
    model = Manufactor
    success_url = reverse_lazy('manufactors')

    def get_context_data(self, **kwargs):
        context = super(ManufactorDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context
