import logging

from django.db import connection
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.loggers.query_logger import QueryLogger
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts
from .models import Manufactor

active_tab = '\'manufactors\''
log_name = consts.logs['manufactor']
init_log(log_name)
logger = logging.getLogger(log_name)


class ManufactorListView(generic.ListView):
    model = Manufactor
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            context = super(ManufactorListView, self).get_context_data(**kwargs)
            context['great_manufactor_name'] = 'ASUS manufactor'
            context['great_manufactor_summary'] = 'Summary for ASUS manufactor'
            context['active_tab'] = active_tab
        logger.info(str(ql))

        return context


# CRUD
class ManufactorDetailView(generic.DetailView):
    model = Manufactor

    def get_context_data(self, **kwargs):
        context = super(ManufactorDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_object(self, queryset=None):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            obj = super(ManufactorDetailView, self).get_object()
        logger.info(str(ql))

        return obj


class ManufactorCreateView(CreateView):
    model = Manufactor
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ManufactorCreateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(ManufactorCreateView, self).form_valid(form)
        logger.info(str(ql))

        return response


class ManufactorUpdateView(UpdateView):
    model = Manufactor
    fields = ['name', 'summary']

    def get_context_data(self, **kwargs):
        context = super(ManufactorUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def form_valid(self, form):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(ManufactorUpdateView, self).form_valid(form)
        logger.info(str(ql))

        return response


class ManufactorDeleteView(DeleteView):
    model = Manufactor
    success_url = reverse_lazy('manufactors')

    def get_context_data(self, **kwargs):
        context = super(ManufactorDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def delete(self, request, *args, **kwargs):
        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            response = super(ManufactorDeleteView, self).delete(request, *args, **kwargs)
        logger.info(str(ql))

        return response
