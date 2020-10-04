from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import FormView

from catalog.mixins import PageTitleMixin
from catalog.loggers.query_logger_config import init_log
from catalog.utils import consts
from catalog.utils.main import query_log
from item.models import Item
from item_issue.forms import IssueForm
from item_issue.models import ItemIssue

active_tab = '\'item_issues\''
active_tab_items = '\'items\''
log_name = consts.logs['item']
init_log(log_name)


@method_decorator(login_required, name='dispatch')
class ItemIssueSendView(PageTitleMixin, FormView):
    form_class = IssueForm
    success_url = reverse_lazy('items')
    template_name = 'item_issue/item_issue.html'
    page_title = 'Сделать заявку'
    active_tab = active_tab_items

    @query_log(log_name=log_name)
    def form_valid(self, form):
        selected_item_id = form.cleaned_data['select_item']
        selected_item = Item.objects.get(item_id=selected_item_id)
        if selected_item:
            ItemIssue.objects.create(item=selected_item, created_by=self.request.user)
        else:
            raise ValidationError(_('Выбран неверный товар'), code='invalid')

        return super(ItemIssueSendView, self).form_valid(form)


class ItemIssueListView(PageTitleMixin, generic.ListView):
    model = ItemIssue
    paginate_by = 10
    page_title = 'Заявки'
    active_tab = active_tab


class ItemIssueDetailView(PageTitleMixin, generic.DetailView):
    model = ItemIssue
    page_title = 'Заявка'
    active_tab = active_tab
