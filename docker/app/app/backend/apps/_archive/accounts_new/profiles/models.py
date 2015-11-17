from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class AccountsUser(AbstractUser):
    USERNAME_FIELD = 'username'  # name of field on the User that is used as the unique identfier.
    activation_key = models.CharField(_('activation key'), max_length=40)
    # Extra Profile Fields
    is_subscribed = models.BooleanField(_('subscribed'), default=False, help_text=_('Designates whether the user can is subscribed to the newsletter.'))
    ###########################################################################
    # Note Django User has the following fields so dont Duplicate!
    ###########################################################################
    # id
    # username
    # first_name
    # last_name
    # email
    # password
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined
    ###########################################################################
    # future
    #bio = models.TextField()
    #failed_login_attempts = models.PositiveIntegerField(default=0, editable=False)
    #last_login_attempt_ip = models.CharField(default='', max_length=45, editable=False)
