from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^manufactors/$', views.ManufactorListView.as_view(), name='manufactors'),
    url(r'^manufactor/(?P<pk>\d+)$', views.ManufactorDetailView.as_view(), name='manufactor_detail'),
    url(r'^manufactor/create/$', views.ManufactorCreateView.as_view(), name='manufactor_create'),
    url(r'^manufactor/(?P<pk>\d+)/update/$', views.ManufactorUpdateView.as_view(), name='manufactor_update'),
    url(r'^manufactor/(?P<pk>\d+)/delete/$', views.ManufactorDeleteView.as_view(), name='manufactor_delete'),
    url(r'^manufactor/go-to-google/$', RedirectView.as_view(url='https://google.ru'), name='go-to-google'),

    url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    url(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create'),
    url(r'^category/(?P<pk>\d+)/update/$', views.CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete'),

    url(r'^items/$', views.ItemListView.as_view(), name='items'),
    url(r'^item/(?P<pk>[-\w]+)$', views.ItemDetailView.as_view(), name='item_detail'),
    url(r'^item/counter/(?P<pk>[-\w]+)$', views.ItemCounterRedirectView.as_view(), name='item_counter'),
    url(r'^item/create/$', views.ItemCreateView.as_view(), name='item_create'),
    url(r'^item/(?P<pk>[-\w]+)/update/$', views.ItemUpdateView.as_view(), name='item_update'),
    url(r'^item/(?P<pk>[-\w]+)/delete/$', views.ItemDeleteView.as_view(), name='item_delete'),
    url(r'^items/news/$', views.ItemNewsListView.as_view(), name='item_news'),
    url(r'^items/ne_lookup/$', views.ItemListNEView.as_view(), name='item_ne'),
    url(r'^items/abs_lookup/$', views.ItemListABSView.as_view(), name='item_abs'),
    url(r'^items/send_issue/$', views.ItemIssueView.as_view(), name='item_issue_send'),
    url(r'^items/item_issues/$', views.ItemIssueListView.as_view(), name='item_issues'),
    url(r'^items/item_issue/(?P<pk>\d+)$', views.ItemIssueDetailView.as_view(), name='item_issue_detail'),
    # url(r'^items/to_csv/$', views.ItemExportView.as_view(), name='items_to_csv'),
    # url(r'^items/to_csv/$', views.items_large_to_csv_view, name='items_to_csv'),
    url(r'^items/to_csv/$', views.items_to_csv_by_template_view, name='items_to_csv'),
    url(r'^item_to_basket/(?P<pk>[-\w]+)$', views.AddItemToBasketRedirectView.as_view(), name="item_to_basket"),
    url(r'^orders/basket/$', views.BasketListView.as_view(), name='basket'),
    url(r'^orders/make_order/$', views.CreateOrderFromBasketRedirectView.as_view(), name='make_order'),
    url(r'^orders/rm_item_from_basket/(?P<pk>\d+)$', views.rm_item_from_basket_view, name="rm_item_from_basket"),

    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'^order/(?P<pk>[-\w]+)$', views.show_order_detail_view, name='order_detail'),
    url(r'^ajax/calculate_price/$', views.calculate_price, name='calculate_price'),
    url(r'^ajax/calculate_price/(?P<orderitem>[-\w]+)/$', views.calculate_price, name='calculate_price'),
    url(r'^remove_items/', views.remove_order_detail_items_view, name="remove_items"),
    url(r'^order/(?P<pk>[-\w]+)/delete/$', views.order_confirm_delete_form, name='order_delete'),
    url(r'^orderitem/create/(?P<order_id>[-\w]+)$', views.orderitem_create_view, name='orderitem_create'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update/$', views.orderitem_update_view, name='orderitem_update'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update_save/$', views.orderitem_update_save_view, name='orderitem_update_save'),
    url(r'^orderitem/(?P<pk>[-\w]+)/delete/$', views.OrderItemDeleteView.as_view(), name='orderItem_delete'),

    url(r'^categories_raw/$', views.category_raw, name='categories_raw'),
    url(r'^categories_raw_one/(?P<pk>[-\w]+)$', views.category_raw_one, name='categories_raw_one'),
    url(r'^categories_raw_all/$', views.category_raw_all, name='categories_raw_all'),
    url(r'^categories_raw_by_func/$', views.category_raw_by_func, name='categories_raw_by_func'),
]
