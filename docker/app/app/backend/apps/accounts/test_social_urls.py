"""
    accounts.test_social_urls
    =========================

    URLs for testing purposes ONLY

    you can add to TestCase / APITestCase:

    def ExampleTestClass(TestCase):
        urls = 'accounts.test_social_urls'

"""
from django.conf.urls import patterns, url
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from .urls import urlpatterns
from .registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

urlpatterns += patterns(
    '',
    url(r'^social-login/facebook/$', FacebookLogin.as_view(), name='fb_login'),
)
