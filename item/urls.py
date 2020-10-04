from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^items/$', views.ItemListView.as_view(), name='items'),
    url(r'^item/(?P<pk>[-\w]+)$', views.ItemDetailView.as_view(), name='item_detail'),
    url(r'^item/counter/(?P<pk>[-\w]+)$', views.ItemCounterRedirectView.as_view(), name='item_counter'),
    url(r'^item/create/$', views.ItemCreateView.as_view(), name='item_create'),
    url(r'^item/(?P<pk>[-\w]+)/update/$', views.ItemUpdateView.as_view(), name='item_update'),
    url(r'^item/(?P<pk>[-\w]+)/delete/$', views.ItemDeleteView.as_view(), name='item_delete'),
    url(r'^items/news/$', views.ItemNewsListView.as_view(), name='item_news'),
    url(r'^items/ne_lookup/$', views.ItemListNEView.as_view(), name='item_ne'),
    url(r'^items/abs_lookup/$', views.ItemListABSView.as_view(), name='item_abs'),
    # url(r'^items/to_csv/$', views.ItemExportView.as_view(), name='items_to_csv'),
    # url(r'^items/to_csv/$', views.items_large_to_csv_view, name='items_to_csv'),
    url(r'^items/to_csv/$', views.items_to_csv_by_template_view, name='items_to_csv'),
]
