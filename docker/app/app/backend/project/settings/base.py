#!/usr/bin/env python
"""
This is the project main settings file. (Source controlled).
If you need to override a setting locally, use local_settings.py.
"""
GENERATOR_DOCKERIZED_DJANGO_POLYMER_VERSION = '<%= generator_version %>'
import os
import sys
import logging

from project.utils import logger


# Django settings for project.
DEBUG = True  # As of Django 1.5 all logging messages reaching the django logger are sent to Console if (DEBUG=True)

# General Directory Structure
# +++ apps
#   ++ someApp
#       ++ templatetags
#           -- someAppTags.py
#       - models.py
#       - urls.py
#       - views.py
#       - utils.py
#   ++ someOtherApp
#       ++ templatetags
#           -- someOtherAppTags.py
#       - models.py
#       - urls.py
#       - views.py
#       - utils.py
# +++ project
#   ++ settings
#       - base.py (THIS FILE)
#       - dev.py
#       - global.py* (optional)
#   ++ templates
#       # someApp
#           - someTemplate.html
#   ++ test_factories
#       - usefulFactoryScript.py
#   ++ utils
#       - usefulFunctions.py
#   ++ views
#       - mixins.py
#   ++ static
#       - staticFile.html/css/png
#   ++ media
#   - urls.py
#   - views.py

DATABASES = {
    'default': {
        'ENGINE':   os.environ.get('DB_ENGINE'),                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     os.environ.get('DB_NAME'),                  # Or path to database file if using sqlite3.
        'USER':     os.environ.get('DB_USER'),                  # Not used with sqlite3.
        'PASSWORD': os.environ.get('DB_PASS'),              # Not used with sqlite3.
        'HOST':     os.environ.get('DB_HOST'),                  # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     os.environ.get('DB_PORT'),                  # Set to empty string for default. Not used with sqlite3.
    }
}

# ============================================================================ #
# Main Paths
# ============================================================================ #
# Make filepaths relative to settings. This dynamically discovers the path to the project
PROJECT_ROOT = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)
APP_ROOT = os.path.join(SITE_ROOT, 'apps')
# Add App/Library Path
sys.path.append(APP_ROOT)

# ---------------------------------------------------------------------------- #
# General
# ---------------------------------------------------------------------------- #
# Make this unique, and don't share it with anybody.
# (This should be unique if this page was used created using generator-django-polymer)
SECRET_KEY = '<%= secret_key %>'

ADMINS = ((os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')),)

MANAGERS = ADMINS

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

import django.conf.global_settings as DEFAULT_SETTINGS

#TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
#          'django.core.context_processors.request',
#)


ROOT_URLCONF = 'project.urls'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# ---------------------------------------------------------------------------- #
# Media / Static
# ---------------------------------------------------------------------------- #
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# use "manage.py collectstatic"    collects to STATIC_ROOT
STATIC_ROOT = os.path.join(PROJECT_ROOT, '_auto_static')

# URL prefix for static files. Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files (absolute)
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
# Other ways
#STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# ---------------------------------------------------------------------------- #
# Templating
# ---------------------------------------------------------------------------- #
# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
# )

# NOTE: It makes sense to keep all templates under /templates/<app> for easier use.
#       The applications in this project dont need to portable so this decision makes sense.
# For the sake of keeping the ability to add templates under an application we add the
# following code: (but it is not technically needed)
# Dir Structure
# + someApplication
#       + templates
#           + someApplication
#               - someTemplate.html
#TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'), )

# ---------------------------------------------------------------------------- #
# Fixtures
# ---------------------------------------------------------------------------- #
# The list of directories to search for fixtures
# Note: It's bad practice to use fixtures so uncomment this.
#       Use test factories or migrations for data instead
#FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'fixtures'))

# ---------------------------------------------------------------------------- #
# Installed Applications
# ---------------------------------------------------------------------------- #
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PATH_APPS = (
    'django_extensions',
    'mptt',
    'taggit',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
)

# HACK BEFORE DJANGO.CONTRIB.AUTH
LOCAL_APPS = (
    'accounts',
    'stats',
    # 'accounts.rest_auth',
    # 'accounts.profiles',
    'blog',
    # 'content',
    # 'mailbot',
    # 'search',
    # 'shop',
    # 'cms',
    # 'admin',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PATH_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------- #
# Third Party App Dependencies
# ---------------------------------------------------------------------------- #
##############################################################################
# Accounts / Regisratiorn App
AUTH_USER_MODEL = 'accounts.AccountsUser'
REGISTRATION_OPEN = True

ACCOUNT_AUTHENTICATION_METHOD = 'username'

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
)

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     )
# }

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
   ),
   'PAGINATE_BY': 10,
}

# If you are running Django 1.8+, specify the context processors
# as follows:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Already defined Django-related contexts here
            'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                 'django.core.context_processors.request',
                # `allauth` needs this from django
                'django.template.context_processors.request',

            ],
            'debug': True,    
        },
    },
]


ACCOUNTS_PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM = True
#PASSWORD_RESET_NOTIFY_EMAIL_NOT_IN_SYSTEM













# Search App
REDIS_HOST = '192.168.99.100'

# Search App
REDIS_HOST = 'redis'








##############################################################################
# Reg App
# Actually from django.contrib.auth  (AUTHENTICATION)
#LOGIN_URL = '/accounts/auth/login/'
#LOGIN_REDIRECT_URL = '/accounts/auth/login/'  # (global_settings.py)  '/users/profile/' - - default
# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7

#REGISTRATION_OPEN = True


# http://django-allauth.readthedocs.org/en/latest/configuration.html









##############################################################################
# Django Shop
SHOP_SHIPPING_FLAT_RATE = '-30'
#SHOP_SHIPPING_BACKENDS = [
#    'shop.shipping.backends.flat_rate.FlatRateShipping',
#]
SHOP_PAYMENT_BACKENDS = [
     'payment.shipping.SkipShippingBackend',
  #  'shop.payment.backends.pay_on_delivery.PayOnDeliveryBackend'
]
SHOP_CART_MODIFIERS = [
    'shop_simplevariations.cart_modifier.ProductOptionsModifier',
    'payment.modifiers.FixedShippingCosts',
    'payment.modifiers.FixedTaxRate',
]

##############################################################################
# CORS Django App
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
#CORS_ALLOW_ALL_ORIGIN = True
#CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?$', )

##############################################################################
# Django Dynamic Fixture
DDF_DEFAULT_DATA_FIXTURE = 'sequential'  # or 'static_sequential' or 'random' or 'path.to.yout.DataFixtureClass'
IMPORT_DDF_MODELS = ''
DDF_FILL_NULLABLE_FIELDS = True

##############################################################################
# Django Nose
# overrides global settings for default test runner
# (we dont want to use default django testing as it has many limitations )
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ---------------------------------------------------------------------------- #
# LOGGING - logging configuration
# ---------------------------------------------------------------------------- #
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(created)f %(filename)s %(funcName)s %(levelname)s %(module)s %(pathname)s %(process)d %(processName)s  %(lineno)s %(levelno)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'custom': {
            '()':  logger.DjangoProjectLogFormatter,
        },

    },
    # special filter: e.g. only log when debug=False (Django only provides two filters) (make a custom if needed)
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse',
         }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'filename': SITE_ROOT + '/log/' + 'project' + '.log',
            'formatter': 'verbose',
        },
        'null': {
            'level': 'INFO',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    # This is the logger you use e.g. logging.getLogger(django)
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'project_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
