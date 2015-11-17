#!/usr/bin/env python
"""
    settings.local
    ==============

    This is the settings file that you use when you're working on the project locally.
    Local development-specific settings include DEBUG mode, log level and activation of developer
    tools like django-debug-toolbar.
"""
from .base import *

DEBUG = True  # As of Django 1.5 all logging messages reaching the django logger are sent to Console if (DEBUG=True)
DEV_SETTINGS = os.environ.get('DJ_DEV_SETTINGS')
LOG_LEVEL = os.environ.get('DJ_LOG_LEVEL')


# need to add logging settings here for debug