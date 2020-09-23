from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .mixins import PageTitleMixin
from .models import Manufactor
from .loggers.query_logger_config import init_log
from .utils import consts
from .utils.main import query_log

active_tab = '\'manufactors\''
log_name = consts.logs['manufactor']
init_log(log_name)


class ManufactorListView(PageTitleMixin, generic.ListView):
    model = Manufactor
    paginate_by = 10
    page_title = 'Производители'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def get_context_data(self, **kwargs):
        context = super(ManufactorListView, self).get_context_data(**kwargs)
        context['great_manufactor_name'] = 'ASUS manufactor'
        context['great_manufactor_summary'] = 'Summary for ASUS manufactor'
        return context


# CRUD
class ManufactorDetailView(PageTitleMixin, generic.DetailView):
    model = Manufactor
    page_title = 'Производитель'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def get_object(self, queryset=None):
        return super(ManufactorDetailView, self).get_object()


class ManufactorCreateView(PageTitleMixin, CreateView):
    model = Manufactor
    fields = '__all__'
    page_title = 'Создать производителя'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def form_valid(self, form):
        return super(ManufactorCreateView, self).form_valid(form)


class ManufactorUpdateView(PageTitleMixin, UpdateView):
    model = Manufactor
    fields = ['name', 'summary']
    page_title = 'Редактировать производителя'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def form_valid(self, form):
        return super(ManufactorUpdateView, self).form_valid(form)


class ManufactorDeleteView(PageTitleMixin, DeleteView):
    model = Manufactor
    success_url = reverse_lazy('manufactors')
    page_title = 'Удалить производителя'
    active_tab = active_tab

    @query_log(log_name=log_name)
    def delete(self, request, *args, **kwargs):
        return super(ManufactorDeleteView, self).delete(request, *args, **kwargs)
