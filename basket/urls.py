from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^item_to_basket/(?P<pk>[-\w]+)$', views.AddItemToBasketRedirectView.as_view(), name="item_to_basket"),
    url(r'^orders/basket/$', views.BasketListView.as_view(), name='basket'),
    url(r'^orders/make_order/$', views.CreateOrderFromBasketRedirectView.as_view(), name='make_order'),
    url(r'^orders/rm_item_from_basket/(?P<pk>\d+)$', views.rm_item_from_basket_view, name="rm_item_from_basket"),
]
