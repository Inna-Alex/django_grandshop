from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^manufactors/$', views.ManufactorListView.as_view(), name='manufactors'),
    url(r'^manufactor/(?P<pk>\d+)$', views.ManufactorDetailView.as_view(), name='manufactor_detail'),
    url(r'^manufactor/create/$', views.ManufactorCreate.as_view(), name='manufactor_create'),
    url(r'^manufactor/(?P<pk>\d+)/update/$', views.ManufactorUpdate.as_view(), name='manufactor_update'),
    url(r'^manufactor/(?P<pk>\d+)/delete/$', views.ManufactorDelete.as_view(), name='manufactor_delete'),
    
    url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    url(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^category/create/$', views.CategoryCreate.as_view(), name='category_create'),
    url(r'^category/(?P<pk>\d+)/update/$', views.CategoryUpdate.as_view(), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDelete.as_view(), name='category_delete'),
    
    url(r'^items/$', views.ItemListView.as_view(), name='items'),
    url(r'^item/(?P<pk>[-\w]+)$', views.ItemDetailView.as_view(), name='item_detail'),
    url(r'^item/create/$', views.ItemCreate.as_view(), name='item_create'),
    url(r'^item/(?P<pk>[-\w]+)/update/$', views.ItemUpdate.as_view(), name='item_update'),
    url(r'^item/(?P<pk>[-\w]+)/delete/$', views.ItemDelete.as_view(), name='item_delete'),
    
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'^order/(?P<pk>[-\w]+)$', views.show_order_detail_form, name='order_detail'),
    url(r'^ajax/calculate_price/$', views.calculate_price, name='calculate_price'),
    url(r'^ajax/calculate_price/(?P<orderitem>[-\w]+)/$', views.calculate_price, name='calculate_price'),
    url(r'^remove_items/', views.remove_order_detail_items, name="remove_items"),
    url(r'^orderitems/$', views.OrderItemListView.as_view(), name='orderitems'),
    url(r'^orderitem/(?P<pk>[-\w]+)$', views.OrderItemDetailView.as_view(), name='orderitem_detail'),
    url(r'^order/create/$', views.OrderCreate.as_view(), name='order_create'),
    url(r'^order/(?P<pk>[-\w]+)/update/$', views.OrderUpdate.as_view(), name='order_update'),
    url(r'^order/(?P<pk>[-\w]+)/delete/$', views.order_confirm_delete_form, name='order_delete'),
    url(r'^orderitem/create/(?P<order_id>[-\w]+)$', views.orderitem_create_view, name='orderitem_create'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update/$', views.orderitem_update_view, name='orderitem_update'),
    url(r'^orderitem/(?P<pk>[-\w]+)/update_save/$', views.orderitem_update_save_view, name='orderitem_update_save'),  
    url(r'^orderitem/(?P<pk>[-\w]+)/delete/$', views.OrderItemDelete.as_view(), name='orderItem_delete'),
]
