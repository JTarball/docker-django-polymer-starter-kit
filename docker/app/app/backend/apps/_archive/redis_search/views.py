from django.template import RequestContext
from django.shortcuts import render_to_response

from redis_search import utils
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
        
        

