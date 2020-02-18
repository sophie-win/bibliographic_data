from django.conf.urls import url

from .views import (
    GetNodesData,

    GetCountries)

urlpatterns = [
    url(r'^nodes[/]?$', GetNodesData.as_view(), name='get_nodes_data'),
    url(r'^countries[/]?$', GetCountries.as_view(), name='get_countries'),
]
