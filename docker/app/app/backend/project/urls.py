from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views
from accounts.views import SendConfirmationEmailView
from allauth.account.views import ConfirmEmailView
admin.autodiscover()

###############################################################################################################
## APP Url Imports
##############################################################################################################
#from search import urls as urls_search
from blog import urls as urls_blog
#from blog.views import PostEditView
from accounts import urls as urls_accounts
from search import urls as urls_search
from stats import urls as urls_stats
#from content import urls as urls_content
#from users import urls as urls_users
#from .views_proj import *

urlpatterns = patterns('',
    # url(r'^home/', include(urls_content, namespace="content")),
    #url(r'^a', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include(urls_search, namespace="search")),
    url(r'^stats/', include(urls_stats, namespace="stats")),
    url(r'^blog/', include(urls_blog, namespace="blog")),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^preview', PostEditView.as_view(), name="preview"),
    url(r'^polymer/home/polymer/language/polymer-result', TemplateView.as_view(template_name="index4.html")),
    url(r'^polymer_test', TemplateView.as_view(template_name="index5.html")),
    url(r'^polymer_list', TemplateView.as_view(template_name="index6.html")),
    url(r'^personal', TemplateView.as_view(template_name="index7.html")),
    #url(r'^@j/', include(urls_content, namespace="content")),
    #(r'^grappelli/', include('grappelli.urls')),
    # ==================================== #
    # User Profile & Registration
    # ==================================== #
    #(r'^users/profile/', include(urls_users)),
    url(r'^accounts/', include(urls_accounts, namespace="accounts")),
    # need this !!! as is as allatth iwll call 
    url(r'^account-confirm-email/(?P<key>\w+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^account-email-verification-sent/$', TemplateView.as_view(), name='account_email_verification_sent'),


    #url(r'^regression/', include(urls_regression, namespace="regression"))
        # this url is used to generate email content
    #url(r'^password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.password_reset_confirm,
    #    name='password_reset_confirm'),
    url('^', include('django.contrib.auth.urls')),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # djang-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py#L190
    #url(r'^account-confirm-email/(?P<key>\w+)/$', ConfirmEmailView.as_view(),
    #    name='account_confirm_email'),
)


# ==================================== #
# Static Pages for Dev Only
# ==================================== #
# if DEBUG (This is implicit)  i.e. DEBUG must be set to TRUE

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()

# ==================================== #
# Other Pages
# ==================================== #
# 404  - defaults to 404.html
# 500  - defaults to 500.html
# 403  - defaults to 403.html in the root of the template directory
#handler404 = 'project.views.home'
