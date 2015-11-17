"""

    blog.urls
    =========

"""
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import PostViewSet

# Should have the following
# post_list - a list of all publish blogs (readonly)
# post_list_all - a list of all blogs
# post_detail - if author,staff, superadmin can edit else read only
post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_list_by_year = PostViewSet.as_view({
    'get': 'posts_by_year',
})
post_list_by_tag = PostViewSet.as_view({
    'get': 'posts_by_tag',
})
post_list_by_user = PostViewSet.as_view({
    'get': 'posts_by_user',
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', post_list, name='list'),
    url(r'^user/(?P<user>[\w-]+)/$', post_list_by_user, name="list_user"),
    url(r'^year/(?P<year>[0-9]{4})/$', post_list_by_year, name="list_year"),
    url(r'^tag/(?P<tag>[\w-]+)/$', post_list_by_tag, name="list_tag"),
    url(r'^post/(?P<slug>[\w-]+)/$', post_detail, name='detail'),

])
