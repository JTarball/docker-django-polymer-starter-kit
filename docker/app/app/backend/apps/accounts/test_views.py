"""
    accounts.test_views
    ===================

    Tests the REST API calls.

    Add more specific social registration tests
"""
import responses

from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from allauth.account import app_settings
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL

from .serializers import LoginSerializer


class TestAccounts(APITestCase):
    """ Tests normal use - non social login. """

    def setUp(self):
        self.login_url = reverse('accounts:rest_login')
        self.logout_url = reverse('accounts:rest_logout')
        self.register_url = reverse('accounts:rest_register')
        self.password_reset_url = reverse('accounts:rest_password_reset')
        self.rest_password_reset_confirm_url = reverse('accounts:rest_password_reset_confirm')
        self.password_change_url = reverse('accounts:rest_password_change')
        self.verify_url = reverse('accounts:rest_verify_email')
        self.user_url = reverse('accounts:rest_user_details')
        self.client = APIClient()
        self.reusable_user_data = {'username': 'admin', 'email': 'admin@email.com', 'password': 'password12'}
        self.reusable_user_data_change_password = {'username': 'admin', 'email': 'admin@email.com', 'password': 'password_same'}
        self.reusable_register_user_data = {'username': 'admin', 'email': 'admin@email.com', 'password1': 'password12', 'password2': 'password12'}
        self.reusable_register_user_data1 = {'username': 'admin1', 'email': 'admin1@email.com', 'password1': 'password12', 'password2': 'password12'}
        self.reusable_register_user_data_no_username = {'email': 'admin@email.com', 'password1': 'password12', 'password2': 'password12'}
        self.reusable_register_user_data_no_email = {'username': 'admin', 'password1': 'password12', 'password2': 'password12'}
        self.change_password_data_incorrect = {"new_password1": "password_not_same", "new_password2": "password_same"}
        self.change_password_data = {"new_password1": "password_same", "new_password2": "password_same"}
        self.change_password_data_old_password_field_enabled = {"old_password": "password12", "new_password1": "password_same", "new_password2": "password_same"}

    def create_user_and_login(self):
        """ Helper function to create a basic user, login and assign token credentials. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, "Snap! Basic Login has failed with a helper function 'create_user_and_login'. Something is really wrong here.")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['key'])

    def _generate_uid_and_token(self, user):
        result = {}
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        from django import VERSION
        if VERSION[1] == 5:
            from django.utils.http import int_to_base36
            result['uid'] = int_to_base36(user.pk)
        else:
            from django.utils.http import urlsafe_base64_encode
            result['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        result['token'] = default_token_generator.make_token(user)
        return result

    def cleanUp(self):
        pass

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_login_basic_username_auth_method(self):
        """ Tests basic functionality of login with authentication method of username. """
        # Assumes you provide username,password and returns a token
        get_user_model().objects.create_user('admin3', '', 'password12')
        data = {"username": 'admin3', "email": "", "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.content)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL,
                       ACCOUNT_EMAIL_REQUIRED=True)
    def test_login_basic_email_auth_method(self):
        """ Tests basic functionality of login with authentication method of email. """
        # Assumes you provide username,password and returns a token
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        data = {"username": '', "email": "email.login@gmail.com", "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.content)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_basic_username_email_auth_method(self):
        """ Tests basic functionality of login with authentication method of username or email. """
        # Assumes you provide username,password and returns a token
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        # Check email
        data = {"username": '', "email": "email.login@gmail.com", "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Check username
        data = {"username": 'admin', "email": '', "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.content)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_login_auth_method_username_fail_no_users_in_db(self):
        """ Tests login fails with a 400 when no users in db for login auth method of 'username'. """
        serializer = LoginSerializer({'username': 'admin', 'password': 'password12'})
        response = self.client.post(self.login_url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_login_email_auth_method_fail_no_users_in_db(self):
        """ Tests login fails with a 400 when no users in db for login auth method of 'email'. """
        serializer = LoginSerializer({'username': 'admin', 'password': 'password12'})
        response = self.client.post(self.login_url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_username_email_auth_method_fail_no_users_in_db(self):
        """ Tests login fails with a 400 when no users in db for login auth method of 'username_email'. """
        serializer = LoginSerializer({'username': 'admin', 'password': 'password12'})
        response = self.client.post(self.login_url, serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def common_test_login_fail_incorrect_change(self):
        # Create user, login and try and change password INCORRECTLY
        self.create_user_and_login()
        self.client.post(self.password_change_url, data=self.change_password_data_incorrect, format='json')
        # Remove credentials
        self.client.credentials()
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.content)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_login_username_auth_method_fail_incorrect_password_change(self):
        """ Tests login fails with an incorrect/invalid password change (login auth username). """
        self.common_test_login_fail_incorrect_change()

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_login_email_auth_method_fail_incorrect_password_change(self):
        """ Tests login fails with an incorrect/invalid password change (login auth email). """
        self.common_test_login_fail_incorrect_change()

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_username_email_auth_method_fail_incorrect_password_change(self):
        """ Tests login fails with an incorrect/invalid password change (login auth username_email). """
        self.common_test_login_fail_incorrect_change()

    def common_test_login_correct_password_change(self):
        # Create user, login and try and change password successfully
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, data=self.change_password_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Remove credentials
        self.client.credentials()
        response = self.client.post(self.login_url, self.reusable_user_data_change_password, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.content)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_login_username_auth_method_correct_password_change(self):
        """ Tests login is succesful with a correct password change (login auth username). """
        self.common_test_login_correct_password_change()

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_login_email_auth_method_correct_password_change(self):
        """ Tests login is succesful with a correct password change (login auth email). """
        self.common_test_login_correct_password_change()

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_username_email_auth_method_correct_password_change(self):
        """ Tests login is succesful with a correct password change (login auth username_email). """
        self.common_test_login_correct_password_change()

    def test_login_fail_no_input(self):
        """ Tests login fails when you provide no username and no email (login auth username_email). """
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        data = {"username": '', "email": '', "password": ''}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_login_username_auth_method_fail_no_input(self):
        """ Tests login fails when you provide no username (login auth username). """
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        data = {"username": '', "email": "email.login@gmail.com", "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_login_email_auth_method_fail_no_input(self):
        """ Tests login fails when you provide no username (login auth email). """
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        data = {"username": "admin", "email": '', "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_login_username_email_auth_method_fail_no_input(self):
        """ Tests login fails when you provide no username and no email (login auth username_email). """
        get_user_model().objects.create_user('admin', 'email.login@gmail.com', 'password12')
        data = {"username": '', "email": '', "password": 'password12'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)





        # need to check for token
        # test login with password change
        # test login with wrong password chaneg if fails

    def test_logout(self):
        """ Tests basic logout functionality. """
        self.create_user_and_login()
        response = self.client.post(self.logout_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"Successfully logged out."}')

    def test_logout_but_already_logged_out(self):
        """ Tests logout when already logged out. """
        self.create_user_and_login()
        response = self.client.post(self.logout_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"Successfully logged out."}')
        self.client.credentials()  # remember to remove manual token credential
        response = self.client.post(self.logout_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEquals(response.content, '{"success":"Successfully logged out."}')

    def test_change_password_basic(self):
        """ Tests basic functionality of 'change of password'. """
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, data=self.change_password_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"New password has been saved."}')

    def test_change_password_basic_fails_not_authorised(self):
        """ Tests basic functionality of 'change of password' fails if not authorised. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.post(self.password_change_url, data=self.change_password_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.content, '{"detail":"Authentication credentials were not provided."}')

    def common_change_password_login_fail_with_old_password(self, password_change_data):
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, data=password_change_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.client.credentials()  # Remove credentials
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def common_change_password_login_pass_with_new_password(self, password_change_data):
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, password_change_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.client.credentials()  # Remove credentials
        response = self.client.post(self.login_url, self.reusable_user_data_change_password, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def common_change_password_login_fail_with_old_password_pass_with_new_password(self, password_change_data):
        """ Tests change of password with old password fails but new password successes. """
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, password_change_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)
        self.client.credentials()  # Remove credentials
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.login_url, self.reusable_user_data_change_password, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.content)

    def test_change_password_login_fail_with_old_password(self):
        """ Tests change of password with old password. """
        self.common_change_password_login_fail_with_old_password(self.change_password_data)

    def test_change_password_login_pass_with_new_password(self):
        """ Tests change of password with new password. """
        self.common_change_password_login_pass_with_new_password(self.change_password_data)

    def test_change_password_login_fail_with_old_password_pass_with_new_password(self):
        """ Tests change of password with old password fails but new password successes. """
        self.common_change_password_login_fail_with_old_password_pass_with_new_password(self.change_password_data)

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_old_password_field_required_old_password_field_enabled(self):
        """ Tests basic functionality of 'change of password' fails if old password not given as part of input (old password field enabled). """
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, data=self.change_password_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.content, '{"old_password":["This field is required."]}')

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_basic_old_password_field_enabled(self):
        """ Tests basic functionality of 'change of password' (old password enabled). """
        self.create_user_and_login()
        response = self.client.post(self.password_change_url, data=self.change_password_data_old_password_field_enabled, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"New password has been saved."}')

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_basic_fails_not_authorised_old_password_field_enabled(self):
        """ Tests basic functionality of 'change of password' fails if not authorised (old password field enabled). """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.post(self.password_change_url, data=self.change_password_data_old_password_field_enabled, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.content, '{"detail":"Authentication credentials were not provided."}')

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_login_fail_with_old_password_old_password_field_enabled(self):
        """ Tests change of password with old password (old password field enabled). """
        self.common_change_password_login_fail_with_old_password(self.change_password_data_old_password_field_enabled)

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_login_pass_with_new_password_old_password_field_enabled(self):
        """ Tests change of password with new password (old password field enabled). """
        self.common_change_password_login_pass_with_new_password(self.change_password_data_old_password_field_enabled)

    @override_settings(OLD_PASSWORD_FIELD_ENABLED=True)
    def test_change_password_login_fail_with_old_password_pass_with_new_password_old_password_field_enabled(self):
        """ Tests change of password with old password fails but new password successes (old password field enabled). """
        self.common_change_password_login_fail_with_old_password_pass_with_new_password(self.change_password_data_old_password_field_enabled)

    """
        Registrations Tests
        ===================
    """
    def common_test_registration_basic(self, data):
        response = self.client.post(self.register_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, response.content)
        return response

    @override_settings(ACCOUNT_EMAIL_REQUIRED=True, ACCOUNT_USERNAME_REQUIRED=True)
    def test_registration_basic(self):
        """ Tests basic functionality of registration. """
        self.common_test_registration_basic(self.reusable_register_user_data)

    @override_settings(ACCOUNT_EMAIL_REQUIRED=True, ACCOUNT_USERNAME_REQUIRED=False)
    def test_registration_basic_no_username(self):
        """ Tests basic functionality of registration (no username required). """
        self.common_test_registration_basic(self.reusable_register_user_data_no_username)

    @override_settings(ACCOUNT_EMAIL_REQUIRED=False, ACCOUNT_USERNAME_REQUIRED=True)
    def test_registration_basic_no_email(self):
        """ Tests basic functionality of registration (no username required). """
        self.common_test_registration_basic(self.reusable_register_user_data_no_email)

    @override_settings(ACCOUNTS_REGISTRATION_OPEN=False)
    def test_registration_basic_registration_not_open(self):
        """ Tests basic registration fails if registration is closed. """
        response = self.client.post(self.register_url, self.reusable_register_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none")
    def test_registration_email_verification_not_necessary(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_basic(self.reusable_register_user_data)
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_registration_email_verification_neccessary(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_basic(self.reusable_register_user_data)
        response = self.client.post(self.login_url, self.reusable_user_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def common_test_registration(self):
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'email': 'admin1@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def common_test_registration_email_verification_not_necessary_email(self):
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'email': 'admin1@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def common_test_registration_email_verification_not_necessary_username(self):
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'username': 'admin1', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_registration_email_verification_neccessary_email(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_email_verification_not_necessary_email()

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_registration_email_verification_neccessary_optional_email(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_email_verification_not_necessary_email()

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_registration_email_verification_neccessary_username(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_email_verification_not_necessary_username()

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_registration_email_verification_neccessary_optional_username(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_email_verification_not_necessary_username()

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="none", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_registration_email_verification_neccessary_username_email(self):
        """ Tests you canT log in without email verification for username & email auth. """
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'username': 'admin1', 'email': 'admin1@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_registration_email_verification_neccessary_optional_username_email(self):
        """ Tests you canT log in without email verification for username & email auth. """
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'username': 'admin1', 'email': 'admin1@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_registration_email_verification_necessary_login_fail_username(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'username': 'admin1', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_registration_email_verification_necessary_login_fail_email(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_basic(self.reusable_register_user_data1)
        response = self.client.post(self.login_url, {'email': 'admin1@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_registration_email_verification_necessary_login_fail_username_email(self):
        """ Tests you can log in without email verification """
        self.common_test_registration_basic({'username': 'admin_man', 'email': 'admin1@email.com', 'password1': 'password12', 'password2': 'password12'})
        response = self.client.post(self.login_url, {'username': 'admin_man', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def common_registration_email_verification_neccessary_verified_login(self, login_data):
        mail_count = len(mail.outbox)
        reg_response = self.common_test_registration_basic(self.reusable_register_user_data1)
        self.assertEquals(len(mail.outbox), mail_count + 1)
        new_user = get_user_model().objects.latest('id')
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEquals(login_response.status_code, status.HTTP_400_BAD_REQUEST)
        # verify email
        email_confirmation = new_user.emailaddress_set.get(email=self.reusable_register_user_data1['email']).emailconfirmation_set.order_by('-created')[0]
        verify_response = self.client.post(self.verify_url, {'key': email_confirmation.key}, format='json')
        self.assertEquals(verify_response.status_code, status.HTTP_200_OK)
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEquals(login_response.status_code, status.HTTP_200_OK)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)
    def test_registration_email_verification_neccessary_verified_login_username(self):
        """ Tests you can log in without email verification """
        self.common_registration_email_verification_neccessary_verified_login({'username': 'admin1', 'password': 'password12'})

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)
    def test_registration_email_verification_neccessary_verified_login_email(self):
        """ Tests you can log in without email verification """
        self.common_registration_email_verification_neccessary_verified_login({'email': 'admin1@email.com', 'password': 'password12'})

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory", ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)
    def test_registration_email_verification_neccessary_verified_login_username_email(self):
        """ Tests you can log in without email verification """
        self.common_registration_email_verification_neccessary_verified_login({'username': 'admin1', 'password': 'password12'})

    """
        Password Reset Tests
        ====================
    """
    def test_password_reset(self):
        """ Test basic functionality of password reset. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        payload = {'email': 'admin@email.com'}
        response = self.client.post(self.password_reset_url, payload, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"Password reset e-mail has been sent."}')

    @override_settings(ACCOUNTS_PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM=True)
    def test_password_reset_fail_no_user_with_email_no_notify_not_in_system(self):
        """ Test basic functionality of password reset fails when there is no email on record (notify email not in system). """
        payload = {'email': 'admin@email.com'}
        response = self.client.post(self.password_reset_url, payload, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.content, '{"error":"User with email doesn\'t exist. Did not send reset email."}')

    @override_settings(ACCOUNTS_PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM=False)
    def test_password_reset_no_user_with_email_no_notify_not_in_system(self):
        """ Test basic functionality of password reset fails when there is no email on record. """
        payload = {'email': 'admin@email.com'}
        response = self.client.post(self.password_reset_url, payload, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content, '{"success":"Password reset e-mail has been sent."}')

    def test_password_reset_confirm_fail_invalid_token(self):
        """ Test password reset confirm fails if token is invalid. """
        user = get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        url_kwargs = self._generate_uid_and_token(user)
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'uid': url_kwargs['uid'],
            'token': '-wrong-token-'
        }
        response = self.client.post(self.rest_password_reset_confirm_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.content, '{"token":["Invalid value"]}')

    def test_password_reset_confirm_fail_invalid_uid(self):
        """ Test password reset confirm fails if uid is invalid. """
        user = get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        url_kwargs = self._generate_uid_and_token(user)
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'uid': 0,
            'token': url_kwargs['token']
        }
        response = self.client.post(self.rest_password_reset_confirm_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.content, '{"uid":["Invalid value"]}')

    def test_password_reset_confirm_fail_passwords_not_the_same(self):
        """ Test password reset confirm fails if uid is invalid. """
        user = get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        url_kwargs = self._generate_uid_and_token(user)
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_not_the_same_password',
            'uid': url_kwargs['uid'],
            'token': url_kwargs['token']
        }
        response = self.client.post(self.rest_password_reset_confirm_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.content, '{"new_password2":["The two password fields didn\'t match."]}')

    def test_password_reset_confirm_login(self):
        """ Tests password reset confirm works -> can login afterwards. """
        user = get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        url_kwargs = self._generate_uid_and_token(user)
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'uid': url_kwargs['uid'],
            'token': url_kwargs['token']
        }
        response = self.client.post(self.rest_password_reset_confirm_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.login_url, {'username': 'admin', 'email': 'admin@email.com', 'password': 'new_password'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm_login_fails_with_old_password(self):
        """ Tests password reset confirm fails with old password. """
        user = get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        url_kwargs = self._generate_uid_and_token(user)
        data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
            'uid': url_kwargs['uid'],
            'token': url_kwargs['token']
        }
        response = self.client.post(self.rest_password_reset_confirm_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response = self.client.post(self.login_url, {'username': 'admin', 'email': 'admin@email.com', 'password': 'password12'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
        User Detail Tests
        =================
    """

    def test_user_details_get(self):
        """ Test to retrieve user details. """
        self.create_user_and_login()
        response = self.client.get(self.user_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content,  '{"username":"admin","email":"admin@email.com","first_name":"","last_name":""}')

    def test_user_details_put(self):
        """ Test to put update user details. """
        self.create_user_and_login()
        response = self.client.put(self.user_url, {"username":"changed","email":"changed@email.com","first_name":"changed","last_name":"name"}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content,  '{"username":"changed","email":"changed@email.com","first_name":"changed","last_name":"name"}')

    def test_user_details_patch(self):
        """ Test to patch update user details. """
        self.create_user_and_login()
        response = self.client.patch(self.user_url, {'username': 'changed_username', 'email': 'changed@email.com'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.content,  '{"username":"changed_username","email":"changed@email.com","first_name":"","last_name":""}')

    def test_user_details_put_not_authenticated(self):
        """ Test to put update user details. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.put(self.user_url, {"username":"changed","email":"changed@email.com","first_name":"changed","last_name":"name"}, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_details_patch_not_authenticated(self):
        """ Test to patch update user details. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.patch(self.user_url, {'username': 'changed_username', 'email': 'changed@email.com'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_details_get_not_authenticated(self):
        """ Test to retrieve user details. """
        get_user_model().objects.create_user('admin', 'admin@email.com', 'password12')
        response = self.client.get(self.user_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAccountsSocial(APITestCase):
    """ Tests normal for social login. """

    urls = 'accounts.test_social_urls'

    def setUp(self):
        self.fb_login_url = reverse('fb_login')
        social_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='123123123',
            secret='321321321',
        )
        site = Site.objects.get_current()
        social_app.sites.add(site)
        self.graph_api_url = GRAPH_API_URL + '/me'

    @responses.activate
    def test_social_auth(self):
        """ Tests Social Login. """
        resp_body = '{"id":"123123123123","first_name":"John","gender":"male","last_name":"Smith","link":"https:\\/\\/www.facebook.com\\/john.smith","locale":"en_US","name":"John Smith","timezone":2,"updated_time":"2014-08-13T10:14:38+0000","username":"john.smith","verified":true}'  # noqa
        responses.add(
            responses.GET,
            self.graph_api_url,
            body=resp_body,
            status=200,
            content_type='application/json'
        )

        users_count = get_user_model().objects.all().count()
        response = self.client.post(self.fb_login_url, {'access_token': 'abc123'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

    @responses.activate
    def test_social_auth_only_one_user_created(self):
        """ Tests Social Login. """
        resp_body = '{"id":"123123123123","first_name":"John","gender":"male","last_name":"Smith","link":"https:\\/\\/www.facebook.com\\/john.smith","locale":"en_US","name":"John Smith","timezone":2,"updated_time":"2014-08-13T10:14:38+0000","username":"john.smith","verified":true}'  # noqa
        responses.add(
            responses.GET,
            self.graph_api_url,
            body=resp_body,
            status=200,
            content_type='application/json'
        )

        users_count = get_user_model().objects.all().count()
        response = self.client.post(self.fb_login_url, {'access_token': 'abc123'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        # make sure that second request will not create a new user
        response = self.client.post(self.fb_login_url, {'access_token': 'abc123'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

    @responses.activate
    def test_failed_social_auth(self):
        # fake response
        responses.add(
            responses.GET,
            self.graph_api_url,
            body='',
            status=400,
            content_type='application/json'
        )
        response = self.client.post(self.fb_login_url, {'access_token': 'abc123'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
