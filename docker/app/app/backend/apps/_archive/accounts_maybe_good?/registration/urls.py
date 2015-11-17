"""
URLconf for registration and activation.

If the default behavior of these views is acceptable to you, simply use a line like this in your
 root URLconf to set up the default URLs for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

 ----- AUTOMATIC include from django.contrib.auth.views -----
* User login at ``login/``.
* User logout at ``logout/``.
* The two-step password change at ``password/change/`` and ``password/change/done/``.
* The four-step password reset at ``password/reset/``, ``password/reset/confirm/``,
 ``password/reset/complete/`` and ``password/reset/done/``.
"""
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import Activate, Register, AccountsRegisterView, AjaxRestricted, AjaxStaffRestricted

urlpatterns = patterns('',
                       url(r'^activate/complete/$', TemplateView.as_view(template_name='accounts/activation_complete.html'), name='registration_activation_complete'),
                       url(r'^activate/failed/$', TemplateView.as_view(template_name='accounts/activation_failed.html'), name='registration_activation_failed'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a confusing 404.
                      url(r'^activate/(?P<activation_key>\w+)/$', Activate.as_view(), name='registration_activate'),
                      url(r'^register/$', AccountsRegisterView.as_view(), name='registration_register'),
                      url(r'^register/complete/$', TemplateView.as_view(template_name='accounts/reg_complete.html'), name='registration_complete'),
                      url(r'^register/closed/$', TemplateView.as_view(template_name='accounts/registration_closed.html'), name='registration_disallowed'),
                       )

auth_urls = patterns('',
                     url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='auth_login'),
                     url(r'^loggedin/$', AjaxRestricted.as_view(), name='auth_loggedin'),
                     url(r'^is_staff/$', AjaxStaffRestricted.as_view(), name='auth_is_staff'),
                     url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'}, name='auth_logout'),
                     url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
                     url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
                     url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
                     url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
                     url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
                     url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
  )

urlpatterns += auth_urls
