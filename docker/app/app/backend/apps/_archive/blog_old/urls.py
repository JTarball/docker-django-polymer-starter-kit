"""
URLconf for 'blog' application
"""
from django.conf.urls import patterns, url

from .views import PostListView, PostUserListView, PostYearListView, PostCategoryListView, PostDetailView


urlpatterns = patterns('',
				url(r'^$', PostListView.as_view(), name="list"),
				url(r'^user/(?P<username>[\w-]+)/', PostUserListView.as_view(), name="list_user"),
				url(r'^year/(?P<year>[\w-]+)/', PostYearListView.as_view(), name="list_year"),
				url(r'^category/(?P<category>[\w-]+)/', PostCategoryListView.as_view(), name="list_category"),
				url(r'^post/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="detail")
					  )
