"""
    stats.urls
    ===========

"""
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import line_graph_view, bar_graph_view

urlpatterns = format_suffix_patterns([
    url(r'^graph/line/$', line_graph_view, name='line'),
    url(r'^graph/bar/$', bar_graph_view, name='bar'),
])
