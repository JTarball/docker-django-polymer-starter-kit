"""
    model_factories.py - factories for testing
"""
import string
import threading
from datetime import datetime, date, timedelta
from decimal import Decimal

from django.template.defaultfilters import slugify
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, AutoDataFiller
from django_dynamic_fixture.ddf import DataFixture


class StaticFixtureClass(DataFixture):
    """
    This class create static fixture data.

    NOTE: The aim to test the basic functionality of the uut using dummy data.
           Use Random / Sequential / Boundary / Type fixtures for complex bugs/states.
    """
    # NUMBERS
    def integerfield_config(self, field, key):
        return 387937296437

    def smallintegerfield_config(self, field, key):
        return 27

    def positiveintegerfield_config(self, field, key):
        return 0


    def positivesmallintegerfield_config(self, field, key):
        return 0

    def bigintegerfield_config(self, field, key):
        return -9223372036854775808

    def floatfield_config(self, field, key):
        return float(27)

    def decimalfield_config(self, field, key):
        return Decimal("0.02012")

    # STRINGS
    def charfield_config(self, field, key):
        return unicode(string.printable)

    def textfield_config(self, field, key):
        return self.charfield_config(field, key)

    def slugfield_config(self, field, key):
        return slugify(self.charfield_config(field, key))

    def commaseparatedintegerfield_config(self, field, key):
        return unicode(1, 3, 2, 4, 6, 0, 5, 7, 8, 9)

    # BOOLEAN
    def booleanfield_config(self, field, key):
        return False

    def nullbooleanfield_config(self, field, key):
        return None

    # DATE/TIME RELATED
    def datefield_config(self, field, key):
        return date.today()

    def timefield_config(self, field, key):
        return datetime.now() - timedelta(seconds=10)

    def datetimefield_config(self, field, key):
        return datetime.now()

    # FORMATTED STRINGS
    def emailfield_config(self, field, key):
        return u'test.static_fixture@djangoproject.co.uk'

    def urlfield_config(self, field, key):
        return u'http://www.staticfixtureclass.com'

    def ipaddressfield_config(self, field, key):
        return u'64.233.191.255'

    def xmlfield_config(self, field, key):
        return u'<a>hello this is a static test.</a>'

    # FILES
    def filepathfield_config(self, field, key):
        return u'/home/'

    def filefield_config(self, field, key):
        return unicode(290783)

    def imagefield_config(self, field, key):
        return unicode(290783)


class UserStaticFixtureClass(StaticFixtureClass):
    """
    This class create static fixture data.

    NOTE: Password is raw as we have no hash fixture_algorithms
    TODO: add hash support for passwords
    """

    def charfield_config(self, field, key):
        if field.name == "username":
            return u'user105'
        elif field.name == "first_name":
            return u'Danvir'
        elif field.name == "last_name":
            return u'Guram'
        elif field.name == "password":
            return u'password12'  # need to be set before save
        elif field.name == "name":
            return u'name'
        else:
            print field.name
            return u'dummy'

    def emailfield_config(self, field, key):
        print dir(self)
        return u'danvir.guram@googlemail.com'

    def booleanfield_config(self, field, key):
        if field.name == "is_staff":
            return True
        elif field.name == "is_active":
            return True  # this is the default anyways
        elif field.name == "is_superuser":
            return False  # this is the default anyways
        else:
            return False

    def datetimefield_config(self, field, key):
        if field.name == "last_login":
            return datetime.now() - timedelta(days=5)
        elif field.name == "date_joined":
            return datetime.now() - timedelta(days=10)
        else:
            return datetime.now()


class UserPermissionStaticFixtureClass(SequentialDataFixture):
    """
    This class create static fixture data.

    NOTE: Password is raw as we have no hash fixture_algorithms
    TODO: add hash support for passwords
    """

    def charfield_config(self, field, key):
        if field.name == "name":
            return u'Can add user'
        elif field.name == "codename":
            return u'add_user'
        else:
            return u'dummy'


class UserContentStaticFixtureClass(SequentialDataFixture):
    """
    This class create static fixture data.

    NOTE: Password is raw as we have no hash fixture_algorithms
    TODO: add hash support for passwords
    """

    def charfield_config(self, field, key):
        if field.name == "name":
            return u'user'
        elif field.name == "app_label":
            return u'auth'
        elif field.name == "model":
            return u'user'
        else:
            return u'dummy'


class ProjAutoDataFiller(object):
    """
    Responsibility: generate a unique and sequential value for each key.
    """

    def __init__(self, pattern):
        self.__data_controller_map = {}  # key => counter
        self.__locks = {}  # key => lock
        self.pattern = pattern

    # synchronized by key
    def next(self, key):
        if key not in self.__data_controller_map:
            self.__data_controller_map[key] = 0
            self.__locks[key] = threading.RLock()
        self.__locks[key].acquire()
        self.__data_controller_map[key] += 1
        value = self.__data_controller_map[key]
        print "value", value
        self.__locks[key].release()
        return self.pattern[value]


# it can inherit of SequentialDataFixture, RandomDataFixture etc.
# method names must have the format: FIELDNAME_config
class ProjectDataFixtureClass(SequentialDataFixture):

    def __init__(self):
        self.filler = ProjAutoDataFiller(string.printable)  # '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'

    def get_next_string(self, field, key):
        return self.filler.next(key)

    #def charfield_config(self, field, key):
    #    data = self.get_next_string(field, key)
    #    if field.max_length:
    #        data = unicode("%s" % data * field.max_length)
    #    else:
    #        print 'NO MAX LENGTH'
    #        data = unicode(data)
    #    return data

    # STRINGS
    def charfield_config(self, field, key):
        data = self.get_next_string(field, key)
        return data
        #if field.max_length:
        #    max_value = (10 ** field.max_length) - 1
        #    data = unicode(data % max_value)
        #    data = data[:field.max_length]
        #else:
        #    data = unicode(data)
        #return data



#TODO: error with over max max_length
#TODO: blank data

# it can inherit of SequentialDataFixture, RandomDataFixture etc.
# method names must have the format: FIELDNAME_config

        #self.number_filler = ProjAutoDataFiller([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # numbers
        #self.filler = ProjAutoDataFiller(string.printable)                   # '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        #self.str_letters = ProjAutoDataFiller(string.letters)
        #self.str_punctation = ProjAutoDataFiller(string.punctuation)
        #self.str_whitespace = ProjAutoDataFiller(string.whitespace)
        #self.str_digits = ProjAutoDataFiller(string.digits)
        #self.ascii_filler = ProjAutoDataFiller(string.ascii_letters)             # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #string.printable = combination of string.digits + string.letters + string.punctuation + string.whitespace

