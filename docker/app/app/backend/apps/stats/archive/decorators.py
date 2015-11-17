#!/usr/bin/env python
"""
    stats.decorators
    ================

    The main decorator for adding redis stats

"""
import logging
from datetime import datetime

from django.conf import settings

from redis import Redis

import timeutils

logger = logging.getLogger('project_logger')
#REDIS_HOST = getattr(settings, "REDIS_HOST", '192.168.99.100')
REDIS_HOST = '192.168.99.100'

r = Redis(host=REDIS_HOST)
# Method of stat count calculation
METHOD_MAP = {"add": lambda n, m: n+m,
              "subtract": lambda n, m: n-m,
              "multiply": lambda n, m: n*m,
              "divide": lambda n, m: n/m,
              }


class redis_stat(object):
    """
        Base Redis Stat Class.
        Stat can be updated via own method or via own custom update
        format: <day>:<hour>:<minute>:<second>:<microsecond>:<count>
        TODO: memory usage for this object / Redis optimising of python code testing
    """
    def __new__(typ, *attr_args, **attr_kwargs):
        """ Add function name. """
        self = object.__new__(typ)
        def f2(orig_func):
            def f3(*func_args, **func_kwargs):
                # Take argument list for original function
                return self(*func_args, **func_kwargs)
            f3.func_name = orig_func.func_name
            self.orig_func = orig_func
            self.new_func = f3
            self.__init__(*attr_args, **attr_kwargs)                
            return f3
        return f2

    def __init__(self, rate_limit='100000/s'):
        # Initial state
        self.stat_index = 0                               # The stat z index (the sort order)
        self.stat_count = 0                               # Start stat count
        self.rate_allowance = 0.0                         # Rate allowance (normalised) (needs to be float (i.e not an integer)
        self.rate_limit = timeutils.rate(rate_limit)      # Rate limit in seconds (normalised)
        self.last_save = datetime.now()
        print 'initialised stat: %s' % self.orig_func.__name__
        logger.info('initialised stat: %s' % self.orig_func.__name__)

    def __call__(self, method, value):
        if (self._rate_limiter() or self.stat_index == 0):  # can I update the stat? (rate limited ok or first)
            if self.orig_func(method, value) is None:   # does the stat have its own update method?
                self._calculate_stat_update(method, value)
            else:
                self.stat_count = self.orig_func(method, value)
                self._update_stat(self.stat_count)

    def _calculate_stat_update(self, method, value):
        """Update stats"""
        self.stat_count = METHOD_MAP[method](self.stat_count, value)
        self._update_stat(self.stat_count)

    def _update_stat(self, count):
        """Update stats"""
        self.stat_index += 1
        self.timestamp = "%s:%s:%s:%s:%s" % (self.last_save.day, self.last_save.hour,
                                             self.last_save.minute, self.last_save.second, self.last_save.microsecond)
        # Add to Redis - use index for sort order
        print "%s" % self.orig_func.__name__, "%s:%s" % (self.timestamp, count)
        r.zadd("%s" % self.orig_func.__name__, "%s:%s" % (self.timestamp, count), self.stat_index)

    def _rate_limiter(self):
        """Simple rate limiter function. Returns false if over the rate limit."""
        delta_t_passed = datetime.now() - self.last_save
        self.rate_allowance += delta_t_passed.total_seconds() * self.rate_limit
        if (self.rate_allowance < 1.0):
            return False
        else:
            self.last_save = datetime.now()  # is this acceptible? there is a slight delay
            self.rate_allowance -= 1.0        # reset rate_limit
            return True


@redis_stat(rate_limit='100000/s')
def example_stat(method, value):
    """How to update this stat"""
    return 1
    
@redis_stat()
def example2_stat(method, value):
    """How to update this stat"""
    pass    
    
if __name__ == '__main__':
        example_stat("add",1)
        example2_stat("add",2)
        example_stat("add",3)
        example2_stat("add",4)
        print r.zrangebyscore("example2_stat", float("-inf"), float("inf"))