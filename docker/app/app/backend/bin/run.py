#!/usr/bin/env python

import sys
import os
# import traceback

# from django.core.handlers.wsgi import WSGIHandler
# from django.core.management import call_command
# from django.core.signals import got_request_exception

import site

# Add apps to directory  - can put all apps under /apps
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)
site.addsitedir(path('apps'))


sys.path.append('..')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings.base'


# def exception_printer(sender, **kwargs):
#     traceback.print_exc()

# got_request_exception.connect(exception_printer)

# call_command('migrate')
# application = WSGIHandler()

# if __name__ == '__main__':
#     import eventlet
#     from eventlet import wsgi
#     print 'Serving on 8000...'
#     wsgi.server(eventlet.listen(('', 8000)), application)





"""
WSGI config for docker_django project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.base")

application = get_wsgi_application()