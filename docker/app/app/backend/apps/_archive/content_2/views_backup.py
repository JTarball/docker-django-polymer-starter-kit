import logging

from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from content.models import Post, Language, Category, SubCategory

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
        return self.model.objects.live_by_subcategory(self.kwargs['language'])


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
    pass


class PostListView(PublishedPostsMixin, ListView):
   pass


class PostUserListView(PublishedUserPostsMixin, ListView):
    pass


class PostYearListView(PublishedYearPostsMixin, ListView):
    pass





# Abstract Class
# TODO: explanation needed about this classes and how they relate to the url
class PjaxMixin(AjaxResponseMixin):
    # Is there info in url -- FIXME: need to write a better description
    path_language = ""
    path_category = ""
    path_subcategory = ""
    pjax_template_name = ''      # This is the html template for the pjax response (html for partial update)



# NOTE: Need to inherit from this class otherwises you might get key errors
#       from template tags 
class PjaxMixin(AjaxResponseMixin):
    # Is there info in url -- FIXME: need to write a better description
    path_language = ""
    path_category = ""
    path_subcategory = ""

    pjax_template_name = ''

    # def _add_path_info(self, *args, **kwargs):
    #     print "add path info!!!!!!!!!!!!!!!!!"
    #     if self.queryset is None:
    #         self.object_list = self.get_queryset()
    #         context = self.get_context_data(object_list=self.object_list)
    #     else:
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #     if 'language' in kwargs:
    #         context['path_language'] = kwargs['language']
    #     else:
    #         context['path_language'] = ''

    #     if 'category' in kwargs:
    #         context['path_category'] = kwargs['category']
    #     else:
    #         context['path_category'] = ' '

    #     if 'subcategory' in kwargs:
    #         context['path_subcategory'] = kwargs['subcategory']
    #     else:
    #         context['path_subcategory'] = ' '
    #     return context


    def get_context_data(self, **kwargs):
        context = super(PjaxMixin, self).get_context_data(**kwargs)
        context['path_language'] = self.path_language
        context['path_category'] = self.path_category
        context['path_subcategory'] = self.path_subcategory
        return context

    def get(self, request, *args, **kwargs):
        logger.info('Name of View: %s' % self.__class__)
        logger.info('Request: %s' % self.request)
        print args, kwargs, "jsdjkfjsk"

        if 'language' in kwargs:
            self.path_language = kwargs['language']

        if 'category' in kwargs:
            self.path_category = kwargs['category']

        if 'subcategory' in kwargs:
            self.path_subcategory = kwargs['subcategory']

        print self.request.is_ajax()
        #if self.request.is_ajax():
        print args, kwargs
        logger.info('category')
        
        context = self.get_context_data(**kwargs)
        return render_to_response( self.pjax_template_name, context, context_instance = RequestContext(request, { 'pjax': request.META.get('HTTP_X_PJAX'),}), mimetype='application/javascript')
        #else:
        #    a = super(PjaxMixin, self).get(request, *args, **kwargs)
        #    return a


    # def get(self, request, *args, **kwargs):
    #     context = self._add_path_info(*args, **kwargs)
    #     if self.request.is_ajax():
    #         print "CONTEXT PATH LANGUAGE", context['path_language']
    #         return render_to_response( self.pjax_template_name, context, 
    #                                    context_instance = RequestContext(request, {
    #     'pjax': request.META.get('HTTP_X_PJAX'),}), mimetype='application/javascript')
    #     else:
    #         print "CONTEXT -------------------", context
    #         return self.render_to_response(context)





class PjaxListMixin(PjaxMixin):
    pass























class LanguageListView(PjaxMixin, ListView):
    model = Language



class LanguageDetailView(PjaxMixin, DetailView):
    slug_field = 'slug'
    model = Language
    slug_url_kwarg = 'language'
    pk_url_kwarg = None
    pjax_template_name = 'content/language_get_ajax.html'


class CategoryDetailView(PjaxMixin, DetailView):
    slug_field = 'slug'
    model = Category
    slug_url_kwarg = 'category'
    pk_url_kwarg = None
    pjax_template_name = 'content/category_get_ajax.html'



class SubCategoryDetailView(PjaxMixin, DetailView):
    slug_field = 'slug'
    model = SubCategory
    slug_url_kwarg = 'subcategory'
    pk_url_kwarg = None


