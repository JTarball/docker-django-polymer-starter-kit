from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
   #url( r'^', views.ajax_user_search, name = 'demo_index' ),
	url( r'^$', views.ajax_search, name = 'ajax_search' ), 
)