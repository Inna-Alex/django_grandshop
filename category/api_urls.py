from django.conf.urls import url

from .api_views import CategoryViewSet

urlpatterns = [
    url(r'^categories/$', CategoryViewSet.as_view({
        'get': 'list', 'post': 'create', 'patch': 'partial_update'
        }), name='categories_list_api'),
    url(r'^categories/(?P<pk>\d+)$', CategoryViewSet.as_view({
        'get': 'retrieve', 'patch': 'partial_update',
        'delete': 'destroy'}), name='categories_object_api'),
]
