"""

    blog.urls
    =========

"""
from django.conf.urls import patterns, url

from blog.views import PostListView, PostDetailView


urlpatterns = patterns('',
    url(r'^', PostListView.as_view(), name="list"),
    url(r'^/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="detail"),
)
