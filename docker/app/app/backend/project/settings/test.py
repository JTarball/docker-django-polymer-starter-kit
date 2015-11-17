"""
    project.settings.test
    =====================

    Project Test Settings for Test Environment Only

    Mostly derived from base.py settings - override where needed
    The aim is to keep Test settings as simple as possible

"""
from project.settings.base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG  # above, you idiot!

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-US'
SITE_ID = 1
USE_L10N = False
USE_TZ = False

SECRET_KEY = 'local'

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#ROOT_URLCONF = 'project.views.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use console instead of setuping up an email server
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# MIDDLEWARE_CLASSES = [
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# TEMPLATE_CONTEXT_PROCESSORS = [
#     'django.contrib.auth.context_processors.auth',
#     'django.core.context_processors.i18n',
#     'django.core.context_processors.media',
#     'django.core.context_processors.static',
#     'django.core.context_processors.tz',
#     'django.core.context_processors.request',
#     'django.contrib.messages.context_processors.messages'
# ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# Override
INSTALLED_APPS += (
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
#     'accounts',
#     'blog',
#     'south',
     'django_nose',
     'tests',
#     'project.views.tests',
 # imports models for test only
    
)

print INSTALLED_APPS

# Django nose settings

#NOSE_ARGS = (
#    '--with-coverage',
#    '--cover-package=.'
#)

ACCOUNT_EMAIL_VERIFICATION="none"
#ACCOUNT_EMAIL_REQUIRED=True


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

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
        'level': 'DEBUG',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 30,
        'filename': SITE_ROOT + '/log/' + 'project' + '.log',
                'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    # This is the logger you use e.g. logging.getLogger(django)
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'project_logger': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'test_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
