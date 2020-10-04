from django.conf.urls import url

from . import order_item_views
from . import order_views


urlpatterns = [
    url(r'^orders/$', order_views.OrderListView.as_view(), name='orders'),
    url(r'^order/(?P<pk>[-\w]+)$', order_item_views.show_order_detail_view, name='order_detail'),
    url(r'^order/(?P<pk>[-\w]+)/get_payed/$', order_views.order_get_payed, name='order_get_payed'),
    url(r'^ajax/calculate_price/$', order_item_views.calculate_price, name='calculate_price'),
    url(r'^ajax/calculate_price/(?P<orderitem>[-\w]+)/$', order_item_views.calculate_price, name='calculate_price'),
    url(r'^remove_items/', order_item_views.remove_order_detail_items_view, name="remove_items"),
    url(r'^order/(?P<pk>[-\w]+)/delete/$', order_views.order_confirm_delete_form, name='order_delete'),
    url(r'^orderitem/create/(?P<order_id>[-\w]+)$', order_item_views.orderitem_create_view, name='orderitem_create'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update/$', order_item_views.orderitem_update_view, name='orderitem_update'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update_save/$', order_item_views.orderitem_update_save_view, name='orderitem_update_save'),
    url(r'^orderitem/(?P<pk>[-\w]+)/delete/$', order_item_views.OrderItemDeleteView.as_view(), name='orderItem_delete'),
]
