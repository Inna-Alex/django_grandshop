from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^manufactors/$', views.ManufactorListView.as_view(), name='manufactors'),
    url(r'^manufactor/(?P<pk>\d+)$', views.ManufactorDetailView.as_view(), name='manufactor_detail'),
    url(r'^manufactor/create/$', views.ManufactorCreateView.as_view(), name='manufactor_create'),
    url(r'^manufactor/(?P<pk>\d+)/update/$', views.ManufactorUpdateView.as_view(), name='manufactor_update'),
    url(r'^manufactor/(?P<pk>\d+)/delete/$', views.ManufactorDeleteView.as_view(), name='manufactor_delete'),
    url(r'^manufactor/go-to-google/$', RedirectView.as_view(url='https://google.ru'), name='go-to-google'),
]
