#!/usr/bin/env python
"""
    utils.logger
    -------------

    Common Logging Functionality

    Note: 
    We use the python logging functionality for both log messages and stats
    No need to create an instance here. Let Django handle it - sorting out the formatting is enough.

"""

import logging
import logging.handlers
import os

from colours import _c as colour_codes


def prettify(method):
    """Return a pretty representation of a method for use with logging

        Args:
            method      Bound method instance

        Returns:
            string      in the form MyClass.my_method
    """
    rs = ""
    if hasattr(method, "im_self") and method.__dict__.has_key('__self__'):
        rs += str(method.__self__.__class__.__name__)
    elif hasattr(method, "im_self") and method.__dict__.has_key('__class__'):
        rs += str(method.__class__.__name__)

    if hasattr(method, "im_func") and method.__dict__.has_key('__func__'):
        rs += '.' + method.__func__.__name__

    if not rs and hasattr(method, 'func_name'):
        rs += method.func_name
    return rs


class DjangoProjectLogFormatter(logging.Formatter):
    """
        Enforce a consistent log message style for the entire django project to aid debugging
    """
    # Clearly the colour of the message is hugely important!
    _level2ansi = {
        logging.DEBUG   : colour_codes.grey,                     # GreyFgnd
        logging.INFO    : colour_codes.green,                    # GreenFgnd
        logging.WARNING : colour_codes.yellow,                   # YellowFgnd
        logging.ERROR   : colour_codes.red,                      # RedFgnd
        logging.CRITICAL: colour_codes.red + colour_codes.bold   # RedFgnd Bold
        }

    def __init__(self, useANSI=True, *args, **kwargs):

        logging.Formatter.__init__(self, *args, **kwargs)

        if useANSI:
            self._fmtstr = "\x1b[0m%(timestr)s %(ansi)s %(levelstr)s\x1b[0m %(namestr)s %(ansi)s%(module_dir)8s\x1b[0m %(fileinfo)8s %(ansi)s%(msgstr)8s\x1b[0m"
        else:
            self._fmtstr = "%(timestr)s %(levelstr)s %(namestr)s %(fileinfo)s %(msgstr)s"

    def format(self, record):
        d = {}
        split_str = os.path.dirname(record.pathname).split('/')
        d['fileinfo'] = "%s:%s:%s" % (record.filename, str(record.lineno).ljust(4), record.funcName.ljust(30))
        d['timestr'] = self.formatTime(record)
        d['levelstr'] = record.levelname.ljust(7)
        # DSG NOTE: Django app name comes from project tree structure of apps/app_name/python_file.py  e.g. ./apps/content/views.py   django app name is content
        d['module_dir'] = split_str[len(split_str)-1]   # ASSUMPTION: THIS IS THE DJANGO APP NAME
        d['module'] = record.module
        d['namestr'] = record.name.ljust(10)
        d['msgstr'] = (record.msg % record.args).rstrip()
        d['ansi'] = DjangoProjectLogFormatter._level2ansi[record.levelno]
        return self._fmtstr % d

