from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    #url( r'^', views.ajax_user_search, name = 'demo_index' ),
    #url( r'^$', views.ajax_search, name = 'ajax_search' ), 
    #url( r'^$', views.SearchRedisView.as_view(), name = 'ajax_search' ), 
    url( r'^autosuggestions/$', views.AutoCompleteSuggestionsView.as_view(), name = 'autosuggestions' ), 
    url( r'^resultsquery/$', views.SearchQueryPjaxView.as_view(), name = 'results' ), 
)