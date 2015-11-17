"""
URLconf for 'blog' application
"""
from django.conf.urls import patterns, url

from .views import PostNodeListView, PostNodeRootListView, PostNodeLanguageListView, PostUserListView, PostYearListView, PostCategoryListView, PostDetailView, PostEditView,  CommentCreateView


urlpatterns = patterns('',
				#url(r'^', PostNodeListView.as_view(), name="list"),
				#url(r'^/preview/$', PostEditView.as_view(), name="preview"),
				#url(r'^/preview/(?P<slug>[\w-]+)/$', PostEditView.as_view(), name="preview"),
				url(r'^/comment/add/$', CommentCreateView.as_view(), name="addcomment"),
				url(r'^/comment/list/$', CommentCreateView.as_view(), name="comment_list"),
				url(r'^/$', PostNodeRootListView.as_view(), name="root"),
				url(r'^/(?P<language>[\w-]+)/$', PostNodeLanguageListView.as_view(), name="language"),
				url(r'^/(?P<language>[\w-]+)/(?P<parent>[\w-]+)/$', PostNodeListView.as_view(), name="listsmall"),
				url(r'^/(?P<language>[\w-]+)/([\w-]+)/(?P<parent>[\w-]+)/$', PostNodeListView.as_view(), name="list"),
				url(r'^/(?P<language>[\w-]+)/(?P<parent>[\w-]+)/(?P<slug>[\w-]+)', PostDetailView.as_view(), name="detail"),
				#url(r'^/(?P<language>[\w-]+)/([\w-]+)/(?P<parent>[\w-]+)/(?P<slug>[\w-]+)(\.)', PostDetailView.as_view(), name="detail"),
				
				#url(r'/(?P<parent1>[\w-]+)/(?P<parent>[\w]+)/', PostNodeListView.as_view(), name="list"),
				#url(r'/(?P<parent>[\w-]+)/', PostNodeListView.as_view(), name="list"),

				#url(r'^/(?P<parent>[/\w-]+)/', PostNodeListView.as_view(), name="list"),
				#url(r'^', PostNodeListView.as_view(), name="list"),
				#url(r'^user/(?P<username>[\w-]+)/', PostUserListView.as_view(), name="list_user"),
				#url(r'^year/(?P<year>[\w-]+)/', PostYearListView.as_view(), name="list_year"),
				#url(r'^category/(?P<category>[\w-]+)/', PostCategoryListView.as_view(), name="list_category"),
				#url(r'^post/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="detail")
					  )
