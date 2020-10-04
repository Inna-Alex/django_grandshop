from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_issue/$', views.ItemIssueSendView.as_view(), name='item_issue_send'),
    url(r'^item_issues/$', views.ItemIssueListView.as_view(), name='item_issues'),
    url(r'^item_issue/(?P<pk>\d+)$', views.ItemIssueDetailView.as_view(), name='item_issue_detail'),
]
