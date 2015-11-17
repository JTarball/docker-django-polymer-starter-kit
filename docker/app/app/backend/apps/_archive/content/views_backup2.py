import logging

from django.shortcuts import render_to_response as render_to_resp
from django.shortcuts import HttpResponse
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from content.models import Post, Language, Category, SubCategory, PostNode

from project.views.mixins import AjaxResponseMixin

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
class PostDetailView(PublishedPostsMixin, DetailView):
    slug_arg = None # need to add it (if put kargs in as_view())

    #def get_queryset(self):
    #    return self.model.objects.filter(slug=self.slug)

    def get_object(self,queryset=None):
        try:
            slug = self.slug_arg
            queryset = self.get_queryset()
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{'slug': slug})
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                            {'verbose_name': queryset.model._meta.verbose_name})
        return obj



class PostUserListView(PublishedUserPostsMixin, ListView):
    pass


class PostYearListView(PublishedYearPostsMixin, ListView):
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
            logger.info('PjaxMixin, this is a ajax request.')
            logger.info('%s' % context)
            logger.info('%s' % context['category'].subcategory)
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


