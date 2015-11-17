"""
    search.urls
    ===========

"""
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import autosuggest_view, search_view

urlpatterns = format_suffix_patterns([
    url(r'^autosuggest/$', autosuggest_view, name='autosuggest'),
    url(r'^results/$', search_view, name='search'),
])
