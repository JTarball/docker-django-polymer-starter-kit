

class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'ACCOUNTS_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    @property
    def REGISTRATION_OPEN(self):
        """
        Gets settings REGISTRATION_OPEN. It defines whether registration is allowed.
        Defaults to True if setting doesnt exist.
        """
        return self._setting('REGISTRATION_OPEN', True)  # Defaults to True (if doesnt exist)

    @property
    def PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM(self):
        """ Only relevant when password resetting via email address.
            If true an error message will appear if a user doesn't exist in db for the email address.
            i.e. an email will not be sent / not received by that email address.
        """
        return self._setting('PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM', False)


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys
app_settings = AppSettings('ACCOUNTS_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings