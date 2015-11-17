import logging
from itertools import chain

from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response as render_to_resp
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from project.views.mixins import JSONResponseMixin, AjaxResponseMixin, PjaxResponseMixin, SuperuserRequiredMixin, LoginRequiredMixin, StaffuserRequiredMixin, require_get, require_post
from blog.models import Post, PostNode, Comment
from blog.forms.forms import CommentForm
from blog.utils import cwmarkdown

logger = logging.getLogger('project_logger')


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

#
#
#
#
#
#
#
#
#
#
#
##############################################################################
from django.utils.decorators import method_decorator

class AjaxCompatibleLoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated. 
    Ajax if not

    NOTE: This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()

        if request.is_ajax() and request_method in self.http_method_names:
            handler = getattr(self, '%s_ajax' % request_method, self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)
        else:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AjaxCompatibleStaffuserRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated. 
    Ajax if not

    NOTE: This should be the left-most mixin of a view.
    """
    login_url = settings.LOGIN_REDIRECT_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = 'next'  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # If the request's user is not staff,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(AjaxCompatibleStaffuserRequiredMixin, self).dispatch(request,
            *args, **kwargs)


##############################################################################
# PostNode Views
##############################################################################
class PostNodeListMixin(ListView):
    model = PostNode

    def get(self, request, *args, **kwargs):
        logger.info('%s, this is the get function from %s: %s' % (self.__class__.__name__, self.__module__, self.__doc__))
        return super(PostNodeListMixin, self).get(self,**kwargs)


class PostNodeRootListView(PostNodeListMixin):
    """ This is a view to list of all root nodes. """

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(level=0)[0].get_root().get_siblings(include_self=True)


class PostNodeLanguageListView(PostNodeListMixin):
    """ This is a view to list of languages. """

    def get_queryset(self, **kwargs):
        language = self.kwargs['language']
        # Should be unique but lets be panoroid
        return self.model.objects.filter(slug=language)[0].get_children()


class PostNodeListView(PostNodeListMixin):
    """ This is a view to display a list of PostNodes. """
    par_id = None

    def get_context_data(self, **kwargs):
        context = super(PostNodeListView, self).get_context_data(**kwargs)
        post_list = Post.objects.filter(published=True, node__id=self.par_id)
        context['post_list'] = post_list
        return context

    def get_queryset(self, **kwargs):
        language = self.kwargs['language']
        parent = self.kwargs['parent']
        print language, parent
        node_language = self.model.objects.get(slug=language)
        par = self.model.objects.get(language=node_language.id, slug=parent)
        self.par_id = par.id
        return par.get_children()


##############################################################################
# Post
##############################################################################
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
        print "PublishedPostsMixin"
        return self.model.objects.live()


class PostDetailView(PublishedPostsMixin, DetailView):
    # We need to override the object to take into account language etc
    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     slug_field = self.get_slug_field()
    #     queryset = queryset.filter(**{slug_field: slug})
    #     try:
    #         obj = queryset.get(node__slug=self.kwargs['parent'], node__language=self.kwargs['language'])
    #     except ObjectDoesNotExist:
    #         raise Http404(_(u"No %(verbose_name)s found matching the query") %
    #                       {'verbose_name': queryset.model._meta.verbose_name})
    #     return obj
    pass


class PostEditView(AjaxResponseMixin, View):
    model = Post
    template_name = 'blog/preview.html'

    def get(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        #self.object = self.get_object()
        #context = super(PostEditView, self).get_context_data(**kwargs)
        content = request.GET.get('q')
        print request.GET
        print request.POST
        print "content", content
        preview = cwmarkdown(content)
        print "preview", preview
        return HttpResponse(preview)
        return render_to_resp(self.template_name, context, context_instance=RequestContext(request), mimetype='application/javascript')

    def post(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        #self.object = self.get_object()
        #context = super(PostEditView, self).get_context_data(**kwargs)
        content = request.POST.get('foo')
        print request
        print request.POST
        print "content", content
        preview = cwmarkdown(content)
        print "preview", preview
        return HttpResponse(preview)
        return render_to_resp(self.template_name, context, context_instance=RequestContext(request), mimetype='application/javascript')




# views.py
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

#https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    fields = ['content']

class CommentUpdateView(UpdateView):
    model = CommentForm
    fields = ['content']

#class CommentDeleteView(DeleteView):
#    model = Comment
#    success_url = reverse_lazy('author-list')



class CommentListIDView(JSONResponseMixin, AjaxResponseMixin, View):
    model = Comment

    def get_queryset(self, **kwargs):
        post = Post.object.get(pk=self.kwargs['pk'])
        return post.comments.filter(idname=self.kwargs['idname'])

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        #query = request.GET.get('q')
        #logger.info("get_ajax, Search results: %s from query: %s" % (utils.search_redis(query), query))
        #res = utils.search_redis(query)
        #logger.info("get_ajax, create_context_from_search_results: %s" % utils.create_context_from_search_results(res))
        #return self.render_json_response(utils.create_context_from_search_results(res))



class CommentListView(JSONResponseMixin, AjaxResponseMixin, View):
    model = Comment

    def get_queryset(self, **kwargs):
        post = Post.object.get(pk=self.kwargs['pk'])
        return post.comments

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        



# class AddCommentView(LoginRequiredMixin, View):

#     def post_ajax(self, request, *args, **kwargs):
#         logger.info('%s, this is the post_ajax function from %s' % (self.__class__.__name__, self.__module__))
#         return HttpResponse()
