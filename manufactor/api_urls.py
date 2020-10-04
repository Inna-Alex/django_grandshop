from django.conf.urls import url

from .api_views import ManufactorAPIView

urlpatterns = [
    url(r'^manufactors/$', ManufactorAPIView.as_view(),
        name='manufactors_list_api'),
    url(r'^manufactors/(?P<pk>\d+)$', ManufactorAPIView.as_view(),
        name='manufactor_object_api'),
]
