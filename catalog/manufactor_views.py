from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Manufactor
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts
from catalog.utils.main import query_log

active_tab = '\'manufactors\''
log_name = consts.logs['manufactor']
init_log(log_name)


class ManufactorListView(generic.ListView):
    model = Manufactor
    paginate_by = 10

    @query_log(log_name=log_name)
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

    @query_log(log_name=log_name)
    def get_object(self, queryset=None):
        return super(ManufactorDetailView, self).get_object()


class ManufactorCreateView(CreateView):
    model = Manufactor
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ManufactorCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
    def form_valid(self, form):
        return super(ManufactorCreateView, self).form_valid(form)


class ManufactorUpdateView(UpdateView):
    model = Manufactor
    fields = ['name', 'summary']

    def get_context_data(self, **kwargs):
        context = super(ManufactorUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
    def form_valid(self, form):
        return super(ManufactorUpdateView, self).form_valid(form)


class ManufactorDeleteView(DeleteView):
    model = Manufactor
    success_url = reverse_lazy('manufactors')

    def get_context_data(self, **kwargs):
        context = super(ManufactorDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
    def delete(self, request, *args, **kwargs):
        return super(ManufactorDeleteView, self).delete(request, *args, **kwargs)
