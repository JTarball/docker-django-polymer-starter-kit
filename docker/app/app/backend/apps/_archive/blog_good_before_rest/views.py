'''
    blog.views
    ==========
    Note: As Django is only used as a backend there are no
           template based views. All views are ajax views
           returning json objects of models.
'''
import logging

from django.views.generic import CreateView


from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import PostSerializer
# change to serializers.py!!!!!!!!!!!!!!!!

from project.views.mixins import require_get, AjaxOnlyResponseMixin, AjaxOnlyAPIDetailView, AjaxOnlyAPIListView, AjaxOnlyAPICreateView
from .models import Post
from .forms import PostCreateForm

logger = logging.getLogger('project_logger')


class PublishedPostsMixin():
    model = Post

    def get_queryset(self):
        return self.model.objects.live()


@require_get
class PostListView(PublishedPostsMixin, AjaxOnlyAPIListView):
    pass


@require_get
class PostDetailView(PublishedPostsMixin, AjaxOnlyAPIDetailView):
    pass


class PostCreateView(RetrieveUpdateDestroyAPIView):
    queryset = Flavor.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
