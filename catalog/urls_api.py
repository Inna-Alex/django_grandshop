from django.conf.urls import url

from .category_api_views import CategoryViewSet
from .manufactor_api_views import ManufactorAPIView

urlpatterns = [
    url(r'^manufactors/$', ManufactorAPIView.as_view(),
        name='manufactors_list_api'),
    url(r'^manufactors/(?P<pk>\d+)$', ManufactorAPIView.as_view(),
        name='manufactor_object_api'),
    url(r'^categories/$', CategoryViewSet.as_view({
        'get': 'list', 'post': 'create', 'patch': 'partial_update'
        }), name='categories_list_api'),
    url(r'^categories/(?P<pk>\d+)$', CategoryViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'delete': 'destroy'}), name='categories_object_api'),
]
