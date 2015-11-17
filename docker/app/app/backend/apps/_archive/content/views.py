import logging

from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response as render_to_resp
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotModified
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from content.models import Post, Liker, PostCard, Language, Category, SubCategory, PostNode, Update, Issue, Dependency, Troubleshooting, Comment, CommentCard
from content.templatetags.editor_tags import editor_render_unicode
from .forms.forms_card import PostCardForm
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from project.views.mixins import JSONResponseMixin, AjaxResponseMixin, SuperuserRequiredMixin, LoginRequiredMixin, StaffuserRequiredMixin, require_get, require_post


logger = logging.getLogger('project_logger')


def beautifyData(number):
    """ Turns number into beautiful string.
        e.g.
        1,000,000,000 ---> 1G
        1,000,000     ---> 100M
        10,000        ---> 10K
        10            ---> 10
    """
    if number > 1000000000:
        return str(number/1000000000) + "G"
    elif number > 1000000:
        return str(number/1000000) + "M"
    elif number > 1000:
        return str(number/1000) + "K"
    else:
        return str(number)




class NoPostMsgMixin(object):
    no_post_message = 'Sorry, no posts found.'

    def get_context_data(self, **kwargs):
        """ Get the context for this view. Add No Post Message. """
        context = super(NoPostMsgMixin, self).get_context_data(**kwargs)
        context.update({'no_post_msg':self.no_post_message})
        return context


class PublishedPostsMixin(NoPostMsgMixin):
    model = Post

    def get_queryset(self,  **kwargs):
        print self.kwargs
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


class PublishedLanguagePostsMixin(NoPostMsgMixin):
    no_post_message = 'Sorry, no posts found for category: '
    model = Post

    #def get_queryset(self, **kwargs):
    #    self.no_post_message += self.kwargs['language']
    #    return self.model.objects.live_by_language(language=self.kwargs['language'])


class DirectoryFolderMixin(object):
    def get_context_data(self, **kwargs):
        """ Get the context for this view. Add No Post Message. """
        context = super(DirectoryFolderMixin, self).get_context_data(**kwargs)
        print self
        context.update({'current_url':self.request.path})
        return context

# ============ Views ===================== #
class PostDetailView(AjaxResponseMixin, PublishedPostsMixin, DetailView):
    node_id = None # need to add it (if put kargs in as_view())
    ajax_template_name = 'content/pjax/post_update.html'      # This is the html template for the pjax response (html for partial update)
    #def get_queryset(self):
    #    return self.model.objects.filter(slug=self.slug)

    def get_object(self,queryset=None):
        logger.error('get_object')
        try:
            node_id = self.node_id
            queryset = self.get_queryset()
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{'slug': node_id})
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                            {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get(self, request, *args, **kwargs):
        logger.error('PjaxMixin, this is the get function called from %s' % self.__class__.__name__ )
        self.request = request   # Used in response_to_response
        return super(PostDetailView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.error('PjaxMixin, this is the post function called from %s' % self.__class__.__name__ )
        self.request = request   # Used in response_to_response
        posted_content = self.request.GET.get('post_content')
        save_id = self.request.POST.get('save_id')
        print save_id, posted_content

        model = Post.objects.get(slug=self.node_id)
        if save_id == 'content-main':
            model.content = unicode(posted_content)
        elif save_id == 'content-code-examples':
            model.content_codeexamples = unicode(posted_content)
        elif save_id == 'content-demo':
            model.content_demo = unicode(posted_content)
        elif save_id == 'content-design-decisions':
            model.content_designdecisions = unicode(posted_content)
        elif save_id == 'content-further-learning':
            model.content_furtherlearning = unicode(posted_content)
        elif save_id == 'content-gotchas':
            model.content_gotchas = unicode(posted_content)
        elif save_id == 'content-tricks-tips':
            model.content_trickstips = unicode(posted_content)

        model.save()
        return HttpResponse()




    def render_to_response(self, context):
        """ Override render_to_response of view - if ajax then update pjax style! else normal render response."""
        logger.info('PjaxMixin, this is the render_to_response function call. The context: %s' % context)
        if self.request.is_ajax():
            logger.info('PjaxMixin, this is a ajax request.%s' % context)
            q = self.request.GET.get('q')


            # DSG BIG HACK
            marked = self.request.GET.get('editor')
            if marked == 'content-main':
                context.update({'editor_data': self.get_object().content_markdown})
            elif marked == 'content-code-examples':
                context.update({'editor_data': self.get_object().content_codeexamples})
            elif marked == 'content-demo':
                context.update({'editor_data': self.get_object().content_demo})
            elif marked == 'content-design-decisions':
                context.update({'editor_data': self.get_object().content_designdecisions})
            elif marked == 'content-further-learning':
                context.update({'editor_data': self.get_object().content_furtherlearning})
            elif marked == 'content-gotchas':
                context.update({'editor_data': self.get_object().content_gotchas})
            elif marked == 'content-tricks-tips':
                context.update({'editor_data': self.get_object().content_trickstips})


            if marked is not None:
                return render_to_resp( 'content/editor_update.html', context)
            else:
                context.update({'preview': q})
                return render_to_resp( self.ajax_template_name, context, context_instance = RequestContext(self.request, { 'pjax': self.request.META.get('HTTP_X_PJAX'),}), mimetype='application/javascript')
        else:
            logger.info('PjaxMixin, this is a normal request.')
            cards = PostCard.objects.filter(main_post=self.get_object())
            card_comments = []
            card_smiles = []
            for card in cards:
                no_of_comments = beautifyData(len(CommentCard.objects.filter(post=card)))
                card_comments.append(no_of_comments)
                no_of_likes = beautifyData(card.likes)
                card_smiles.append(no_of_likes)


            zipped_cards = zip(card_comments, card_smiles, cards)
            context.update({'cards': zipped_cards})


            print context
            return super(PostDetailView, self).render_to_response(context)




class PostUserListView(PublishedUserPostsMixin, ListView):
    pass


class PostYearListView(PublishedYearPostsMixin, ListView):
    pass





class SaveContent(AjaxResponseMixin):
    pass


# Abstract Class
# TODO: explanation needed about this classes and how they relate to the url
# ----------------------------------------------------------------------------
class PjaxMixin(AjaxResponseMixin):
    # Is there info in url -- FIXME: need to write a better description
    path_language = ""
    path_category = ""
    path_subcategory = ""
    pjax_template_name = ''      # This is the html template for the pjax response (html for partial update)

    def get(self, request, *args, **kwargs):
        logger.info('PjaxMixin, this is the get function called from %s' % self.__class__.__name__ )
        self.request = request   # Used in response_to_response
        return super(PjaxMixin, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.info('PjaxMixin, this is the get_context_data function call.')
        context = super(PjaxMixin, self).get_context_data(**kwargs)
        logger.info('language %s category %s SubCategory %s' % ( context, self.path_category, self.path_subcategory ))
        context['path_language'] = self.path_language
        context['path_category'] = self.path_category
        context['path_subcategory'] = self.path_subcategory
        return context 

    def render_to_response(self, context):
        """ Override render_to_response of view - if ajax then update pjax style! else normal render response."""
        logger.info('PjaxMixin, this is the render_to_response function call. The context: %s' % context)
        if self.request.is_ajax():
            logger.info('PjaxMixin, this is a ajax request with context %s' % context)
            logger.info('%s' % context)
            return render_to_resp( self.pjax_template_name, context, context_instance = RequestContext(self.request, { 'pjax': self.request.META.get('HTTP_X_PJAX'),}), mimetype='application/javascript')
        else:
            logger.info('PjaxMixin, this is a normal request')
            return super(PjaxMixin, self).render_to_response(context)

# See urls.py for more information but 
# /home /
# /home / language /
# /home / language / category
# /home / language / category / subcategory (note: also of type Category model)
# /home / language / category / page 
# /home / language / category / subcategory (note: also of type Category model) / page
# ----------------------------------------------------------------------------
class LanguageListView(PjaxMixin, ListView):
    """ Pjax ListView to show all languages. """
    model = Language
    pjax_template_name = 'content/pjax/language_list.html'


class CategoryListView(PjaxMixin, ListView):
    model = Category
    pjax_template_name = 'content/pjax/category_list.html'

    def get_queryset(self, **kwargs):
       a = self.kwargs['language']
       return self.model.objects.filter(language__slug=a)


class SubCategoryListView(PjaxMixin, ListView):
    model = SubCategory
    pjax_template_name = 'content/pjax/subcategory_list.html'

    def get_queryset(self, **kwargs):
       return self.model.objects.filter(category__language__slug=self.kwargs['language'], category__slug=self.kwargs['category'])



class LanguageDetailView(PjaxMixin, DetailView):
    """ Pjax DetailView to show all categories for a language. """
    slug_field = 'slug'
    model = Language
    slug_url_kwarg = 'language'
    pk_url_kwarg = None
    pjax_template_name = 'content/language_categories_get_ajax.html'


class CategoryDetailView(PjaxMixin, DetailView):
    """ Pjax DetailView to show all subcategories for a language category. """
    slug_field = 'slug'
    model = Language
    slug_url_kwarg = 'category'
    pk_url_kwarg = None
    pjax_template_name = 'content/language_category_subcategories_get_ajax.html'





def show_genres(request):
    return render_to_resp("content/genres.html",
                          {'nodes':PostNode.objects.all()},
                          context_instance=RequestContext(request))



class PostListView(PublishedPostsMixin, ListView):
    model = Post


class PostNodeListView(PjaxMixin, ListView):
    model = PostNode
    node_id = None # need to add it (if put kargs in as_view())
    pjax_template_name = 'content/pjax/postnode_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostNodeListView, self).get_context_data(**kwargs)
        post_list = Post.objects.filter(published=True, node__id=self.node_id)
        logger.info('%s' % post_list)
        context['post_list'] = post_list
        return context

    def get_queryset(self, **kwargs):
        logger.info('%s' % type(PostNode.objects.get(id=self.node_id).get_children()))
        return PostNode.objects.get(id=self.node_id).get_children()





class PostUpdateView(SuperuserRequiredMixin, UpdateView):
    """ View for creating Account Users. You should be a superuser. """
    model = Post
    node_id = None # need to add it (if put kargs in as_view())
    form_class = PostCardForm
    template_name = 'content/post_edit.html'

    def get_object(self, queryset=None):
        """
        HACKED PK = NODE_ID CAUSE IT WAS QUICK
        """
        print "get object"
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = None
        slug = self.node_id
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj



class EditorView(PjaxMixin):
    pjax_template_name = 'content/pjax/post_update.html'
    #model = Language



class MarkdownEditorView(TemplateView):
    template_name = 'content/editor.html'

from django.contrib.admin.views.decorators import staff_member_required





##
##   PostCard Views
##############################################################################



class CardStatView(AjaxResponseMixin, TemplateView):
    """ Increment Stat in Card. """
    template_name = 'content/ajax/cardstats_update.html'

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        q = self.request.POST.get('stat') # need to use a load 
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        if q == 'click':
            model.views += 1
        elif q == 'like':
            model.likes += 1

        model.save()

        likes = beautifyData(model.likes)
        views = beautifyData(model.views)
        data = {'card': model, 'clicks': views, 'likes': likes}
        return render_to_resp(self.template_name, data, context_instance=RequestContext(request), mimetype='application/javascript')






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

#
## Card Views
##############################################################################
class CardCreateView(LoginRequiredMixin, CreateView):
    """ NOTE: We need to hack the sucess_url because most models in content 
              don't have an get_absolute_url.
              Need to post success_url data
    """
    model = PostCard
    action = "created"
    # Explicitly attached the PostCardForm class
    form_class = PostCardForm

    def get_success_url(self):
        print self.request
        if self.request.POST.get('success_url'):
            return self.request.POST.get('success_url') # MUST GIVE SUCCESS_URL VIA POST FROM FORM
        else:
            return super(CardCreateView, super).get_success_url()


class CardAddCommentView(LoginRequiredMixin, AjaxResponseMixin, View):
    """ Add Comment to Card. """
    ajax_template_name = 'content/postcard/base_open.html'
    no_to_display = 5

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the get_ajax function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        value = self.request.POST.get('value')
        card = PostCard.objects.get(slug=slug)
        user = 'dsg105'

        user_id = auth.get_user_model().objects.get(username=user).id
        print value, card, user_id
        com = CommentCard.objects.create(comment=value, post=card, author_id=user_id)
        com.save()
        # force save on card to update stats
        card.save()
        comments = CommentCard.objects.filter(post=card)
        shows = [True for x in xrange(0, len(comments))]
        # Create Flag and set True in hides array to for displaying more
        load_more = False
        if len(comments) > self.no_to_display: 
            load_more = True
            shows[0:self.no_to_display] = [False for x in xrange(0, self.no_to_display)]
        # zipped data
        zipped_cards = zip(shows, comments)
        data = {'comments': zipped_cards, 'load_more': load_more, 'card': card}
        print "hjhj"
        return render_to_resp(self.ajax_template_name, data, context_instance=RequestContext(request), mimetype='application/javascript')


class CardCommentsView(AjaxResponseMixin, View):
    """ Display Comments from Card. """
    ajax_template_name = 'content/postcard/edit.html'
    no_to_display = 5

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the get_ajax function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        card = PostCard.objects.get(slug=slug)
        comments = CommentCard.objects.filter(post=card)
        shows = [True for x in xrange(0, len(comments))]
        # Create Flag and set True in hides array to for displaying more
        load_more = False
        if len(comments) > self.no_to_display: 
            load_more = True
            shows[0:self.no_to_display] = [False for x in xrange(0, self.no_to_display)]
        # zipped data
        zipped_cards = zip(shows, comments)
        data = {'comments': zipped_cards, 'load_more': load_more, 'card': card}
        return render_to_resp(self.ajax_template_name, data, context_instance=RequestContext(request), mimetype='application/javascript')


class CardDeleteView(StaffuserRequiredMixin, AjaxResponseMixin, View):
    """ Delete Post Card. """

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        model.delete()
        return HttpResponse()


class CardAddClickView(AjaxResponseMixin, View):
    """ Increment View Stat in Card. """
    ajax_template_name = 'content/postcard/stats.html'

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        model.views += 1
        model.save()
        return render_to_resp(self.ajax_template_name, {'card': model}, context_instance=RequestContext(request), mimetype='application/javascript')


class CardAddLikeView(LoginRequiredMixin, AjaxResponseMixin, View):
    """ Increment + Update Like Stat in Card. """
    ajax_template_name = 'content/postcard/stats.html'

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        if not Liker.objects.filter(card_id=model.id, author_id=request.user.id).exists(): 
            model.likes += 1
            Liker.objects.create(card=model, author_id=request.user.id)
        else:
            return HttpResponseNotModified() # Not Modified 304 status code
        model.save()
        return render_to_resp(self.ajax_template_name, {'card': model}, context_instance=RequestContext(request), mimetype='application/javascript')


class CardAddBrokenView(AjaxResponseMixin, View):
    """ Increment Broken Count in Card. """

    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        model.brokens += 1
        model.save()
        return HttpResponse()


class CardCheckImageView(AjaxResponseMixin, View):
    """ Increment Broken Count in Card. """

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        slug = self.kwargs['slug']
        model = PostCard.objects.get(slug=slug)
        model.brokens += 1
        model.save()
        return HttpResponse()


#############################################################################################
@require_get
class PostCommentListView( JSONResponseMixin, ListView):
    model_update = Update
    model_issue = Issue
    model_troubleshooting = Troubleshooting
    model_dependency = Dependency
    model_comment = Comment

    @property
    def model(self):
        logger.info('Property model called')
        #summary_stats = self.request.GET.get('summary_stats')
        #if summary_stats == 'updates':
        #    model = self.model_update
        #elif summary_stats == 'dependencies':
        #    model = self.model_dependency
        #elif summary_stats == 'issues':
        #    model = self.model_issue
        #elif summary_stats == 'troubleshooting':
        #    model = self.model_troubleshooting
        #elif summary_stats == 'comments':
        #    model = self.model_comment
        #else:
        model = self.model_update
        return model

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(post__slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        print self.get_queryset()
        return self.render_json_object_response(self.get_queryset())


@require_post
class CardUpdateView(AjaxResponseMixin, UpdateView):
    model = PostCard

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(main_post__slug=self.kwargs.get('slug'))

    def post_ajax(self, request, *args, **kwargs):
        return self.render_json_object_response(self.get_queryset())


@require_get
class CardListView(JSONResponseMixin, ListView):
    model = PostCard

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(main_post__slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        print "get, CardListView"
        return self.render_json_object_response(self.get_queryset())


@require_get
class CommentCardListView(JSONResponseMixin, ListView):
    model = CommentCard

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(post__slug=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        return self.render_json_object_response(self.get_queryset())




##############################################################################





















class PostCardStatsView(AjaxResponseMixin, TemplateView):
    """ Like ajax """
    template_name = 'content/ajax/cardstats_update.html'


    @login_required
    def delete(self, request, *args, **kwargs):
        print "dsjflskdj"


    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        q = self.request.GET.get('q')
        slug = self.request.POST.get('slug')
        model = PostCard.objects.get(slug=slug)
        if q == 'click':
            model.views += 1
            model.save()
        elif q == 'like':
            model.likes += 1
            model.save()
        elif q == 'delete':
           self.deleteCard(request, *args, **kwargs)

        likes = beautifyData(model.likes)
        views = beautifyData(model.views)
        data = {'card': model, 'clicks': views, 'likes': likes}
        return render_to_resp(self.template_name, data, context_instance=RequestContext(request), mimetype='application/javascript')
        
        







class PostTitleView(AjaxResponseMixin,  TemplateView):
    template_name = 'content/ajax/posttitle_update.html'

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        summary_stats = request.GET.get('summary_stats')
        
        input_placeholder = '' # if empty get template to not display input
        load_more_text = ''
        posts = None
        input_type = 'text'
        editable=True
        if summary_stats == 'updates':
            model = Post.objects.get(slug=kwargs['slug'])
            posts = Update.objects.filter(post=model)
            load_more_text = 'See more of Changelog'
            editable = False
        if summary_stats == 'dependencies':
            model = Post.objects.get(slug=kwargs['slug'])
            posts = Dependency.objects.filter(post=model)
            load_more_text = 'See more Dependencies'
            editable = False
        if summary_stats == 'issues':
            model = Post.objects.get(slug=kwargs['slug'])
            posts = Issue.objects.filter(post=model)
            input_placeholder = 'Search Issues'
            load_more_text = 'See more Issues'
            input_type = 'search'
        if summary_stats == 'troubleshooting':
            model = Post.objects.get(slug=kwargs['slug'])
            posts = Troubleshooting.objects.filter(post=model)
            input_placeholder = 'Search Troubleshooting'
            load_more_text = 'See more from Troubleshooting'
        if summary_stats == 'comments':
            model = Post.objects.get(slug=kwargs['slug'])
            posts = Comment.objects.filter(post=model, is_reply=False)
            input_placeholder = 'Say something nice/cynical'
            load_more_text = 'See more Comments'

        replyarray=[]
        for p in posts: 
            p.forceDateAgo()
            replyarray.append(len(Comment.objects.filter(reply=p)))


        array = []
        i = 0
        for p in posts:
            if i < 5:
                i = i + 1
                array.append(True)
            else:
                array.append(False)
        print array
        zipped = zip(array,replyarray, posts)


        context = super(PostTitleView, self).get_context_data(**kwargs)
        context.update({'input_placeholder': input_placeholder, 'load_more_text': load_more_text,
                        'posts': zipped,
                        'editable': editable,
                        'icon': 'fa fa-clock-o fa-2x',
                        'input_name': input_type, 'input_type': input_type, 
                        })

        return render_to_resp(self.template_name, context, context_instance=RequestContext(request), mimetype='application/javascript')

    def get(self, request, *args, **kwargs):
        logger.error('PjaxMixin, this is the get function called from %s' % self.__class__.__name__ )
            #self.request = request   # Used in response_to_response
        return super(PostTitleView, self).get(self, request, *args, **kwargs)

    #@login_required
    def post_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_post function from %s' % (self.__class__.__name__, self.__module__))
        summary_stats = request.GET.get('summary_stats')
        slug = self.request.POST.get('slug')
        value = self.request.POST.get('value')
        print slug, value

        model = Post.objects.get(slug=slug)
        com = Comment.objects.create(comment=value, post=model)



        com.save()
        return HttpResponse()










#context_instance = RequestContext(self.request, { 'pjax': self.request.META.get('HTTP_X_PJAX'),})

