#!/usr/bin/env python
"""
    stats.redis-stats.py
    ====================


"""
# need to create a bucket service - bucket like server
# redis stat checks can connect on init
# adding to bucket - just adds key to keys (that should be saved in redis for persistence)
# bucketmanager






import logging

import schedule

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


#'<bucket-name>:<stat>, <timestamp:count>'

class Bucket:
    """
        Round robin database bucket.
        Acts like a circular buffer

        rows  - amount of measurements to store, the timespan in seconds of the native resolution equals to :steps*:rows
                "the number of rows in the circular buffer"
        steps - the interval in seconds in which to store measurements
                "the time interval between data(rows) in the circular buffer"
        aggregration - the method of aggregration
           options: 'sum'
    """

    def __init__(self, name, rows, steps, aggregration='sum'):
        self.name = name
        self.rows = rows
        self.steps = steps
        self.aggregration = aggregration
        self.keys = []  # a list of keys for this bucket
        self.job = None
        self.current_row = 0
        self.full = False

    def start(self):
        self.job = schedule.every(self.steps).seconds.do(self._runScheduledTask)
        print "job - %s" % self.job

    def stop(self):
        schedule.cancel_job(self.job)

    def _runScheduledTask(self):
        """ Process new stat value A
            Add new value into buffer. If full need to consolidate values first. """
        print 'hdkjsahfdhsajkdsa'
        #if self.full:
        #    r.zremrangebyrank("")
        #else:
        #    # If buffer is not full, add new stat value and rotate circular buffer
        #    timestamp = '12131324213'
        #    count = 10
        #    key = 'fsdfs'
        #    r.zadd("%s-%s" % (self.name, key), "%s:%s" % (timestamp, count), self.current_row)
        #    self.current_row += 1
        #
        #for key in self.keys:
        #    print key


    def aggregrate(self, key):
        pass

    def addStatKey(self):
        pass



# buckets = {}
# <bucket-name>:keys - the keys for the buckets

BUCKETMANAGER_KEY = 'rrd-buckets'

class BucketManager(object):

    def __init__(self):
        self.buckets = []
        # Restore Redis Server State if exists, else need to create the buckets

        if (self.buckets == []):
            # Create default buckets
            self.add_bucket('rrdbucket1', 10080, 60, 'average')     # 1 week at 1 min interval
            self.add_bucket('rrdbucket2', 10080, 60*15, 'average')  # 1 month at 15 min interval
            self.add_bucket('rrdbucket3', 8760, 60*60, 'average')   # 1 year (365 days) at 1 hour interval

        # Check for changes every 5 minute
        schedule.every(5).minutes.do(self.check_for_new_buckets)

    def check_for_new_buckets(self):
        
        pass





class redis_stat(object):
    """
        Base Redis Stat Class.
        Stat can be updated via own method or via own custom update
        format: <day>:<hour>:<minute>:<second>:<microsecond>:<count>
        TODO: memory usage for this object / Redis optimising of python code testing


        use of rrd buckets for stored historic data

        redis structure  hash table   key - 'self.key'  
        the field should be a relevant name for the stat 
        count - value for the stat

        define buckets for historical data

        - by default should be three buckets
        - need a function for dump fo list of buckets attached to stat (vice-versa)


        - need more logging


    """
    def __init__(self):
        self.key = 'redis-stat'
        self.buckets = []
        # reload redis stat db
        # default create buckets
        self.add_bucket('rrdbucket1', 10080, 60, 'average')     # 1 week at 1 min interval
        self.add_bucket('rrdbucket2', 10080, 60*15, 'average')  # 1 month at 15 min interval
        self.add_bucket('rrdbucket3', 8760, 60*60, 'average')   # 1 year (365 days) at 1 hour interval
        for bucket in self.buckets:
            bucket.start()
        schedule.run_pending()
        pass

    def add_bucket(self, stat_field, rows, steps, aggregation='average'):
        self.buckets.append(Bucket(stat_field, rows, steps, aggregation))

    # def clear_buckets(self, *fields):
    #     """ Clear Buckets for stat field/s. """
    #     if (fields == ()):
    #         fields = r.hkeys(self.key)
    #     for stat_field in fields:
    #         [r.rem(bucket.name + ':' + stat_field) for bucket in self.buckets]
    #     self.buckets = []

    def get(self, stat_field, start=None, end=None, aggregation=None):
        """ Fetch stat values using rrd buckets.
            stat_field  - the stat field in redis
            start       - optional starting timestamp for the timespan to return
            end         - optional ending timestamp for the timespan to return
            aggregation - optional aggregation method when given a timespan

            if start and end are not specified the most current value will be fetched (i.e. not rrd bucketed)
            will be returned only
        """
        pass

    def store(self, stat_field, count, increment=True):
        """ Updates Stat  (increment / replace)
            increment  if True adds count to current value stored at stat_field
                        else if False it replaces the current value
        """
        if increment:
            r.hincrby(self.key, stat_field, count)
        else:
            r.hset(self.key, stat_field, count)

    # def dump(key=None, range=None):
    #     """ Dumps Redis Stats """

    def reset(self, *fields):
        """ Clears stats. If fields is not specified all the stats will be cleared. """
        if (fields == ()):
            fields = r.hkeys(self.key)
        # Clear stat value
        r.hdel(self.key, *fields)
        # Clear all buckets associated with this stat
        # for stat_field in fields:
        #     [r.rem(bucket.name + ':' + stat_field) for bucket in self.buckets]
        # self.buckets = []


if __name__ == '__main__':
        rs = redis_stat()
        rs.store('adas', 1)
        rs.store('adas0', 1)
        #rs.store('adas', 1, False)
        print r.hgetall("redis-stat")
        print r.hkeys("redis-stat")
        rs.reset('adas')
        #rs.reset()
        print "after reset"
        print r.hgetall("redis-stat")
