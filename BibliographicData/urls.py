"""BibliographicData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from fetch_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='publication_graph.html'), name='index'),
    url(r'^fetch/', include(('fetch_api.urls', 'fetch_api'), namespace='fetch_api')),
    url(r'^api/get_suggestions/', views.get_suggestions),
    url(r'^publication_graph', TemplateView.as_view(template_name='publication_graph.html'), name='publication_graph'),
    url(r'^about_us', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    url(r'^genogram', TemplateView.as_view(template_name='genogram.html'), name='genogram'),
    url(r'^api/get_list/', views.get_list),
    url(r'^api/get_json_data/', views.get_json_data),
    url(r'^api/get_family_tree/', views.get_family_tree),
    url(r'^api/get_sample_data/', views.get_sample_data),
    url(r'^api/get_sample_data_for_dropdown/', views.get_sample_data_for_dropdown),
    url(r'^api/expand_more/', views.get_node_relationships)
]
