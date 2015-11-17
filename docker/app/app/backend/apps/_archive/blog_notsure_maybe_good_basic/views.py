'''
    blog.views
    ==========
'''
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from project.views.mixins import JSONResponseMixin, PjaxResponseMixin

from blog.models import Post


class PostListView(JSONResponseMixin, PjaxResponseMixin, ListView):
    model = Post


class PostDetailView(JSONResponseMixin, PjaxResponseMixin, DetailView):
    model = Post
