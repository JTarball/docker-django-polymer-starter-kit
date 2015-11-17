from django_dynamic_fixture import N, G, P, F

from django import test

from accounts.forms import RegistrationForm
from accounts.models import AccountsUser as User


class RegistrationFormTests(test.TestCase):
    """ Tests the Registration Form. """

    def test_reg_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.
        """
        # Create a user so we can verify that duplicate usernames aren't permitted.
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {'data': {'username': 'foo/bar',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'foo',
                      'tos': True},
            'error': ('username', [u"This value may contain only letters, numbers and @/./+/-/_ characters."])},
            # Already-existing username.
            {'data': {'username': 'alice',
                      'email': 'alice@example.com',
                      'password1': 'secret',
                      'password2': 'secret',
                      'tos': True},
            'error': ('username', [u"A user with that username already exists."])},
            # Mismatched passwords.
            {'data': {'username': 'foo',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'bar',
                      'tos': True},
            'error': ('__all__', [u"The two password fields didn't match."])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = RegistrationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        form = RegistrationForm(data={'username': 'foo',
                                      'email': 'foo@example.com',
                                      'password1': 'foo',
                                      'password2': 'foo',
                                      'tos': True})
        self.failUnless(form.is_valid())

    def test_reg_form_tos(self):
        """
        Test that ``RegistrationFormTermsOfService`` requires
        agreement to the terms of service.

        """
        form = RegistrationForm(data={'username': 'foo',
                                                          'email': 'foo@example.com',
                                                          'password1': 'foo',
                                                          'password2': 'foo'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['tos'],
                         [u"You must agree to the terms to register"])

        form = RegistrationForm(data={'username': 'foo',
                                                          'email': 'foo@example.com',
                                                          'password1': 'foo',
                                                          'password2': 'foo',
                                                          'tos': 'on'})
        self.failUnless(form.is_valid())

    def test_reg_form_unique_email(self):
        """
        Test that ``RegistrationForm`` validates uniqueness
        of email addresses.

        """
        # Create a user so we can verify that duplicate addresses aren't permitted.
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = RegistrationForm(data={'username': 'foo',
                                      'email': 'alice@example.com',
                                      'password1': 'foo',
                                      'password2': 'foo',
                                      'tos': True})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'], [u"This email address is already in use. Please supply a different email address."])

        form = RegistrationForm(data={'username': 'foo1',
                                      'email': 'foo@example.com',
                                      'password1': 'foo',
                                      'password2': 'foo',
                                      'tos': True})
        print form.is_valid()
        print form.errors
        self.failUnless(form.is_valid())
