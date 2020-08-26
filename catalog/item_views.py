from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import IssueForm
from .models import Item, ItemIssue

active_tab = '\'items\''


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_queryset(self):
        date_10_days = date.today() - timedelta(days=10)
        return Item.objects.extra(select={'is_recent': 'created_date > %s'},
                                  select_params=(date_10_days,))


# CRUD start
class ItemDetailView(generic.DetailView):
    model = Item
    
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_object(self):
        obj = super(ItemDetailView, self).get_object()
        obj.last_accessed = datetime.now()
        obj.save()
        return obj


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
    fields = ['manufactor', 'category', 'name', 'summary', 'availability',
              'price', 'quantity']

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
# CRUD end


class ItemNewsListView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = 'catalog/item_news_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemNewsListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_queryset(self):
        date_10_days = date.today() - timedelta(days=10)
        return Item.objects.filter(created_date__gte=date_10_days)


class ItemListNEView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = 'catalog/item_ne_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemListNEView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_queryset(self):
        return Item.objects.filter(quantity__ne=5)


class ItemListABSView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = 'catalog/item_abs_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemListABSView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_queryset(self):
        return Item.objects.filter(quantity__abs=5)


class ItemCounterRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'item_detail'

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        item.update_counter_view()
        return super(ItemCounterRedirectView, self).get_redirect_url(*args, **kwargs)


class ItemIssueView(FormView):
    form_class = IssueForm
    success_url = reverse_lazy('items')
    template_name = 'catalog/item_issue.html'

    def get_context_data(self, **kwargs):
        context = super(ItemIssueView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def form_valid(self, form):
        selected_item_id = form.cleaned_data['select_item']
        selected_item = Item.objects.get(item_id=selected_item_id)
        user = self.request.user
        ItemIssue.objects.create(item=selected_item, created_by=user)
        return super().form_valid(form)
