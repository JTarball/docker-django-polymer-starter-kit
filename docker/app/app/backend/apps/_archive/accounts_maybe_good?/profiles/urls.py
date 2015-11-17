from django.conf.urls import patterns, url

from .views import AccountsCreateView, AccountsUpdateView, AccountsUpdateModalView


urlpatterns = patterns('',
                       url(r'^create_user', AccountsCreateView.as_view(), name='accounts_create_user'),
                       url(r'^change_user/(?P<pk>\d+)$', AccountsUpdateView.as_view(), name='update_user'),
                       url(r'^usermodal/(?P<pk>\d+)$', AccountsUpdateModalView.as_view(), name='update_user_modal')
                       )