"""

    blog.urls
    =========

"""
from django.conf.urls import patterns, url

from blog.views import PostListView, PostDetailView, PostCreateView


urlpatterns = patterns('',
                       #url(r'^$', PostListView.as_view(), name="list"),
                       url(r'^post/new', PostCreateView.as_view(), name="create"),
                       url(r'^post/(?P<slug>[/\w-]+)', PostDetailView.as_view(), name="detail"),
                       )
