from django.template import RequestContext
from django.shortcuts import render_to_response

from . import utils

from project.views.mixins import PjaxResponseMixin
# accepts
#   http://domain.com/search/searchquery or
#   http://domain.com/search/?query=searchquery
def ajax_search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        array = []
        for result in utils.searchRedis(q):
          ListDict = {'title':result.title, 'url':result.url, 'category':result.categories.all() }
          array.append(ListDict)

        if q is not None:
            data = { 'results' : array,
                     'length'  : len(array)
                   }
        return render_to_response( 'redis_search/results_4.html', data, 
                                       context_instance = RequestContext(request), mimetype='application/javascript')
    else:     
        return render_to_response('redis_search/index.html', 
                                  context_instance = RequestContext( request ))


from django.views.generic.base import TemplateView, View

from project.views.mixins import AjaxResponseMixin, JSONResponseMixin


class SearchRedisView(AjaxResponseMixin,  TemplateView):
    template_name = 'search/results.html'

    def get_ajax(self, request, *args, **kwargs):
        print request
        q = request.GET.get('query')
        array = []
        for result in utils.searchRedis(q):
            ListDict = {'title': 'this is a example', 'url': 'url', 'category': 'example'}
            array.append(ListDict)
        for result in utils.searchRedis(q):
            print result
        utils.dumpRedis()
        #if q is not None:
        data = {'results': array, 'length': len(array)}
        return render_to_response('search/results_4.html', data, context_instance=RequestContext(request), mimetype='application/javascript')
        #super(SearchRedisView, self).get(request, data=data)
        #

import logging
from itertools import chain

from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response as render_to_resp
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from project.views.mixins import JSONResponseMixin, AjaxResponseMixin, SuperuserRequiredMixin, LoginRequiredMixin, StaffuserRequiredMixin, require_get, require_post
#from blog.models import Post, PostNode
#from blog.utils import cwmarkdown

logger = logging.getLogger('project_logger')

class serf(AjaxResponseMixin, TemplateView):

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        q = request.GET.get('query')
        array = []
        for result in utils.searchRedis(q):
            ListDict = {'title': 'this is a example', 'url': 'url', 'category': 'example'}
            array.append(ListDict)
        for result in utils.searchRedis(q):
            print result
        
        #if q is not None:
        data = {'results': array, 'length': len(array)}
        return HttpResponse(data)




class AutoCompleteSuggestionsView(JSONResponseMixin, AjaxResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        query = request.GET.get('q')
        logger.info("get_ajax, Autocomplete results: %s" % utils.autocomplete_suggestions(query))
        return self.render_json_response(utils.autocomplete_suggestions(query))


class SearchQueryAjaxView(JSONResponseMixin, AjaxResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        logger.info('%s, this is the ajax_get function from %s' % (self.__class__.__name__, self.__module__))
        query = request.GET.get('q')
        logger.info("get_ajax, Search results: %s from query: %s" % (utils.search_redis(query), query))
        res = utils.search_redis(query)
        logger.info("get_ajax, create_context_from_search_results: %s" % utils.create_context_from_search_results(res))
        return self.render_json_response(utils.create_context_from_search_results(res))




class SearchQueryPjaxView(PjaxResponseMixin, TemplateView):
    pjax_template_name = 'search/pjax/search.html'
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        logger.info('SearchQueryPjaxView, this is the get_context_data function call.')
        context = super(PjaxResponseMixin, self).get_context_data(**kwargs)
        # Note PjaxResponseMixin makes request available as a property
        query = self.request.GET.get('q')
        res = utils.search_redis(query)
        context.update({'results': utils.create_context_from_search_results(res)})
        return context 

        
    #    query = request.GET.get('q')
    #    logger.info("get_ajax, Search results: %s from query: %s" % (utils.search_redis(query), query))
    #    res = utils.search_redis(query)
    #    logger.info("get_ajax, create_context_from_search_results: %s" % utils.create_context_from_search_results(res))
        #return self.render_json_response(utils.create_context_from_search_results(res))

