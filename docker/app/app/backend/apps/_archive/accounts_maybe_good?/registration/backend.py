from django.contrib.sites.models import Site, RequestSite

from project.settings import base as settings
from .models import RegistrationProfile
from .forms import RegistrationForm
from . import signals


class AccountsBackend(object):
    """
        1. User signs up, inactive account is created.
        2. Email is sent to user with activation link.
        3. User clicks activation link, account is now active.

        You must have following settings:
          ACCOUNT_ACTIVATION_DAYS  - integer of the number of days a user has to activate their acoount before being disallowed.
          REGISTRATION_OPEN
    """

    def activate(self, activation_key):
        """ Given an activation key try to activate user. Sends Signal if activated. """
        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__, user=activated)
            return [activated, self.post_activation_successful_redirect_url]
        return [False, self.post_activation_failed_redirect_url]  # return False or User / redirect url

    def register(self, request, **kwargs):
        print kwargs['username']
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
        return new_user  # return False or User

    @property
    def registration_allowed(self):
        """
        Gets settings REGISTRATION_OPEN. It defines whether registration is allowed.
        Defaults to True if setting doesnt exist.
        """
        return getattr(settings, "REGISTRATION_OPEN", True)  # Defaults to True (if doesnt exist)

    @property
    def post_registration_redirect(self):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        """
        return 'registration_complete'

    @property
    def post_activation_successful_redirect_url(self):
        """
        Return the name of the URL to redirect to after successful
        account activation.
        """
        return 'registration_activation_complete'

    @property
    def post_activation_failed_redirect_url(self):
        """
        Return the name of the URL to redirect to after successful
        account activation.
        """
        return 'registration_activation_failed'

    @property
    def form(self):
        """ Gets the form used for user registration. """
        return RegistrationForm
