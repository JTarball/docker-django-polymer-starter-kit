from django.views.generic import ListView, DetailView

from blog.models import Post

class NoPostMsgMixin(object):
    no_post_message = 'Sorry, no posts found.'

    def get_context_data(self, **kwargs):
        """ Get the context for this view. Add No Post Message. """
        context = super(NoPostMsgMixin, self).get_context_data(**kwargs)
        context.update({'no_post_msg':self.no_post_message})
        return context


class PublishedPostsMixin(NoPostMsgMixin):
    model = Post

    def get_queryset(self):
        return self.model.objects.live()


class PublishedUserPostsMixin(NoPostMsgMixin):
    no_post_message = 'Sorry, no posts found for user: '
    model = Post

    def get_queryset(self, **kwargs):
        self.no_post_message += self.kwargs['username']
        return self.model.objects.live_by_user(user=self.kwargs['username'])


class PublishedYearPostsMixin(NoPostMsgMixin):
    no_post_message = 'Sorry, no posts found for year: '
    model = Post


    def get_queryset(self, **kwargs):
        self.no_post_message += self.kwargs['year']
        print self.no_post_message
        return self.model.objects.live_by_year(year=self.kwargs['year'])


class PublishedCategoryPostsMixin(NoPostMsgMixin):
    no_post_message = 'Sorry, no posts found for category: '
    model = Post

    def get_queryset(self, **kwargs):
        self.no_post_message += self.kwargs['category']
        return self.model.objects.live_by_category(category=self.kwargs['category'])


# ============ Views ===================== #
class PostDetailView(PublishedPostsMixin, DetailView):
    pass


class PostListView(PublishedPostsMixin, ListView):
   pass


class PostUserListView(PublishedUserPostsMixin, ListView):
    pass


class PostYearListView(PublishedYearPostsMixin, ListView):
    pass


class PostCategoryListView(PublishedCategoryPostsMixin, ListView):
    pass

