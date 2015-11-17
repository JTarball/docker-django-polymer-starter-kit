# Create your views here.
# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponse, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import redis

pool =redis.ConnectionPool(host='localhost', port=6380, db=0)
r = redis.Redis(connection_pool=pool)


def index(request):    
    template = 'redis_stats/index.html'
    a = r.keys("*")
    print a 
    data = {
    'firstname': a,
    'lastname': "m.lastname",
    'username': "m.username",
    }
    #TODO: add if len is 0 blah logging error etc. or if len is more than 1 
    return render_to_response(template, data, RequestContext(request))

