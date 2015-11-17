from django import test


class RegistrationViewTests(test.TestCase):
    """ A class to test registration views. """

    def test_activation(self):
        pass

    def test_registration(self):
        pass

    def test_registration_failed_email(self):
        pass

    def test_post_activation(self):
        pass

    def test_post_registration(self):
        pass

    def test_registration_extra_context(self):
        """
        Passing ``extra_context`` to the ``activate`` view will
        correctly populate the context.

        """
        print self.__doc__
        print "running test: %s" % self._testMethodName
        print dir(self._testMethodName)
        response = self.client.get(reverse('reg_test_activate_extra_context',
                                           kwargs={'activation_key': 'foo'}))
        self.assertEqual(response.context['foo'], 'bar')
        # Callables in extra_context are called to obtain the value.
        self.assertEqual(response.context['callable'], 'called')

    def test_activation_extra_context(self):
        """
        Passing ``extra_context`` to the ``activate`` view will
        correctly populate the context.

        """
        print self.__doc__
        print "running test: %s" % self._testMethodName
        print dir(self._testMethodName)
        response = self.client.get(reverse('reg_test_activate_extra_context',
                                           kwargs={'activation_key': 'foo'}))
        self.assertEqual(response.context['foo'], 'bar')
        # Callables in extra_context are called to obtain the value.
        self.assertEqual(response.context['callable'], 'called')

