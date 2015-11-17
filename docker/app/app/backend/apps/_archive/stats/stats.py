from datetime import datetime, timedelta
from redis import Redis
import time
import logging # import the logging library

import timeutils
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Initialise Redis server
r_server = Redis()
# Method of scount calculation
METHOD_MAP = {"add"         : lambda n,m: n+m,
              "subtract"    : lambda n,m: n-m,
              "multiply"    : lambda n,m: n*m,
              "divide"      : lambda n,m: n/m,
             }

class redis_stat(object):
    """ Base Redis Stat Class. 
        Stat can be updated via own method or via own custom update
        format: <day>:<hour>:<minute>:<second>:<microsecond>:<count>
        TODO: memory usage for this object / Redis 
              optimising of python code
              testing 
    """
    def __new__(typ, *attr_args, **attr_kwargs):
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
            self.sindex = 0 # The stat index 
            self.scount = 0 # Start stat count
            self.rate_allowance = 0 
            self.rate_limit = timeutils.rate(rate_limit) # Rate limit in seconds (normalised)
            self.last_save = datetime.now() 
            logger.info('initialised stat: %s' % self.orig_func.__name__)
    
    def __call__(self, method, value):
        if (self._rate_limiter() or self.sindex == 0): # can I update the stat?
            if self.orig_func(method, value) is None: # does the stat have its own update method?
                self._calc_scount(method, value)
            else:
                self.scount = self.orig_func(method, value)
                self._update_stat(self.scount)
    
    def _calc_scount(self, method, value):
        """Update stats"""
        self.scount = METHOD_MAP[method](self.scount,value)
        self._update_stat(self.scount)
        
    def _update_stat(self, count):
        """Update stats""" 
        self.sindex+=1
        self.timestamp = "%s:%s:%s:%s:%s" %(self.last_save.day, self.last_save.hour,
                                            self.last_save.minute, self.last_save.second, 
                                            self.last_save.microsecond) 
        r_server.zadd("%s" %self.orig_func.__name__, 
                      "%s:%s" %(self.timestamp, count), 
                      self.sindex)
                       
    def _rate_limiter(self):
        """Simple rate limiter function. Returns false if over the rate limit."""
        delta_t_passed = datetime.now() - self.last_save
        self.rate_allowance += delta_t_passed.total_seconds() * self.rate_limit
        if (self.rate_allowance < 1.0): # needs to be float (i.e not an integer)
            return False
        else:
            self.last_save = datetime.now() # is this acceptible? there is a slight delay
            self.rate_allowance -=1.0 # reset rate_limit
            return True

###############################################################################
# Two Examples on Use
###############################################################################
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
###############################################################################    