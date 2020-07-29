from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Manufactor


class ManufactorListView(generic.ListView):
    model = Manufactor
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ManufactorListView, self).get_context_data(**kwargs)
        context['great_manufactor_name'] = 'ASUS manufactor'
        context['great_manufactor_summary'] = 'Summary for ASUS manufactor'
        return context


# CRUD
class ManufactorDetailView(generic.DetailView):
    model = Manufactor


class ManufactorCreate(CreateView):
    model = Manufactor
    fields = '__all__'


class ManufactorUpdate(UpdateView):
    model = Manufactor
    fields = ['name', 'summary']


class ManufactorDelete(DeleteView):
    model = Manufactor
    success_url = reverse_lazy('manufactors')
