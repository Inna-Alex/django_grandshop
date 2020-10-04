from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    url(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create'),
    url(r'^category/(?P<pk>\d+)/update/$', views.CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete'),

    url(r'^categories_raw/$', views.category_raw, name='categories_raw'),
    url(r'^categories_raw_one/(?P<pk>[-\w]+)$', views.category_raw_one, name='categories_raw_one'),
    url(r'^categories_raw_all/$', views.category_raw_all, name='categories_raw_all'),
    url(r'^categories_raw_by_func/$', views.category_raw_by_func, name='categories_raw_by_func'),
]
