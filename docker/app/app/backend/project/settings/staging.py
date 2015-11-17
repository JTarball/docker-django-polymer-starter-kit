#!/usr/bin/env python
"""
    settings.staging
    ================

    Staging version for running a semi-private version of the
    site on a production server. This is where managers and
    client should be looking before your work is moved to
    production
"""
from .base import *

DEBUG = False
