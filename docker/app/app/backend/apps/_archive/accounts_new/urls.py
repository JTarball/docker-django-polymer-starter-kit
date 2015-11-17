"""
URLconf for 'accounts' application
"""
from django.conf.urls import patterns, url, include

from accounts.profiles import urls as urls_profiles
from accounts.rest_auth import urls as urls_reg


urlpatterns = patterns('',
		        #url(r'^', AccountsMainView.as_view()),
		        url(r'^auth/', include(urls_reg)),
				url(r'^backend/', include(urls_profiles)),
                       )
