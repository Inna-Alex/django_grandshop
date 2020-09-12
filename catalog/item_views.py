from datetime import date, datetime, timedelta
import csv
from csv_export.views import CSVExportView

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import IssueForm
from .models import Item, ItemIssue
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts
from catalog.utils.main import query_log

active_tab = '\'items\''
log_name = consts.logs['item']
init_log(log_name)


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 10

    @query_log(log_name=log_name)
    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    def get_queryset(self):
        date_10_days = date.today() - timedelta(days=10)
        queryset = Item.objects.extra(select={'is_recent': 'created_date > %s'},
                                  select_params=(date_10_days,))
        return queryset


# CRUD start
class ItemDetailView(generic.DetailView):
    model = Item
    
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
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

    @query_log(log_name=log_name)
    def form_valid(self, form):
        manufactor = form.cleaned_data['manufactor']
        category = form.cleaned_data['category']
        if manufactor is None:
            raise ValidationError(_('Поле Производитель не должно быть пустым'), code='invalid')
        if category is None:
            raise ValidationError(_('Поле Категория не должно быть пустым'), code='invalid')

        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['manufactor', 'category', 'name', 'summary', 'availability',
              'price', 'quantity']

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
    def form_valid(self, form):
        return super(ItemUpdateView, self).form_valid(form)


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('items')

    def get_context_data(self, **kwargs):
        context = super(ItemDeleteView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab
        return context

    @query_log(log_name=log_name)
    def delete(self, request, *args, **kwargs):
        return super(ItemDeleteView, self).delete(request, *args, **kwargs)
# CRUD end


class ItemNewsListView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = 'catalog/item_news_list.html'

    @query_log(log_name=log_name)
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

    @query_log(log_name=log_name)
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

    @query_log(log_name=log_name)
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


@method_decorator(login_required, name='dispatch')
class ItemIssueView(FormView):
    form_class = IssueForm
    success_url = reverse_lazy('items')
    template_name = 'catalog/item_issue.html'

    def get_context_data(self, **kwargs):
        context = super(ItemIssueView, self).get_context_data(**kwargs)
        context['active_tab'] = active_tab

        return context

    @query_log(log_name=log_name)
    def form_valid(self, form):
        selected_item_id = form.cleaned_data['select_item']
        selected_item = Item.objects.get(item_id=selected_item_id)
        ItemIssue.objects.create(item=selected_item, created_by=self.request.user)

        return super(ItemIssueView, self).form_valid(form)


class ItemExportView(CSVExportView):
    model = Item
    specify_separator = False

    def get_fields(self, queryset):
        fields = ['name', 'summary', 'price', 'quantity', 'availability', 'manufactor', 'category']
        if self.request.user.is_superuser:
            admin_fields = ['created_date', 'last_accessed', 'counter_view', 'counter_buy', 'item_id']
            fields += admin_fields
        return fields

    def get_filename(self, queryset):
        return 'Items-export-{!s}.csv'.format(timezone.now())


class Echo:
    def write(self, value):
        return value


def items_large_to_csv_view(request):
    """
    Items to csv if it's too many
    """
    rows = get_items_to_csv(Item.objects.all(), request.user.is_superuser)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Items-export.csv"'
    return response


def items_to_csv_by_template_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Items-export.csv"'
    is_admin = request.user.is_superuser

    csv_data = get_items_to_csv(Item.objects.all(), is_admin)
    csv_template = 'items_admin_to_csv.txt' if is_admin else 'items_to_csv.txt'

    t = loader.get_template(csv_template)
    c = {'data': csv_data}
    response.write(t.render(c))
    return response


def get_items_to_csv(queryset, is_admin):
    admin_fields = ['created_date', 'last_accessed', 'counter_view', 'counter_buy', 'item_id']
    exclude_fields = admin_fields if not is_admin else []
    opts = queryset.model._meta
    model_fields = [(field.verbose_name, field.name) for field in opts.fields]
    field_verbose_names, field_names = [], []
    for field in model_fields:
        field_v_name, field_name = field
        if field_name not in exclude_fields:
            field_verbose_names.append(field_v_name)
            field_names.append(field_name)

    result = [[getattr(obj, field) for field in field_names] for obj in queryset]
    result.insert(0, field_verbose_names)

    return result
