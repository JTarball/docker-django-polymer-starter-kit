#!/usr/bin/env python
"""
    stats.redis-stats.py
    ====================


"""
# Import Django Settings and App Python Structure
# ===============================================
import os
import sys

try:
    app_dir = os.environ.get('APP_DIR')
except:
    sys.exit("The environment APP_DIR has not been set.")

sys.path.append(app_dir + '/backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.base")

from django.conf import settings
# ======================================================================

import logging
import time

import pandas as pd
from pandas import DataFrame

from bucketmanager import STAT_KEY, RRD_BUCKET_KEY, RRD_BUCKETS_KEY, BUCKET1_ROWS, RRD_DATA_KEY, RRD_BUCKET_STATS_KEY, RRD_BUCKET_CONFIG_KEY, BUCKET_CONFIG

from redis import Redis

from project.utils.logger import DjangoProjectLogFormatter
from project.utils.colours import purple


REDIS_HOST = '192.168.99.100'
r = Redis(host=REDIS_HOST)

handler = logging.FileHandler(settings.SITE_ROOT + '/log/' + 'redis_stat.log')
handler.setFormatter(DjangoProjectLogFormatter())

logger = logging.getLogger('redis_stat')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# NEED TO STOP THE ADDING OF A BUCKET THAN PERIOD IS LESS THAN A MINUTE??????
SHORT_MONTH_MAP = {"1": "J", "2": "F", "3": "M", "4": "A", "5": "M", "6": "J", "7": "J", "8": "A", "9": "S", "10": "O", "11": "N", "12": "D"}


def RRD_STAT_BUCKETS_KEY(stat_name):
    return "%s:%s:buckets" % (STAT_KEY, stat_name)


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
        logger.info(purple("redis_stat instance fired up."))

    def add_bucket(self, bucket_name, stat_field, rows, steps, aggregation='average'):
        """ New """
        r.sadd(RRD_BUCKETS_KEY, bucket_name)
        r.hmset(RRD_BUCKET_KEY + ':' + bucket_name, {'name': bucket_name, 'rows': rows, 'steps': steps, 'aggregation': aggregation})
        r.sadd(RRD_BUCKET_KEY + ':' + bucket_name + ':' + 'keys', stat_field)
        # stat what buckets has
        r.sadd(STAT_KEY + ':' + stat_field + ':buckets', bucket_name)

    def remove_bucket(self, stat_field, bucket_name):
        """ Clear Buckets for stat field/s. """
        r.srem(STAT_KEY + ':' + stat_field + ':buckets', bucket_name)
        r.srem(RRD_BUCKET_KEY + ':' + bucket_name + ':' + 'keys', stat_field)

    def get(self, stat_field, start_date=None, end_date=None, freq='1h'):
        pattern = '%d-%m-%Y %H:%M:%S'
        if start_date is None:
            start = float("-inf")
        else:
            start = int(time.mktime(time.strptime(start_date, pattern)))
        if end_date is None:
            end = float("+inf")
        else:
            end = int(time.mktime(time.strptime(end_date, pattern)))
        # Get all stats for stat_field
        # Get all buckets for stat and combine to one sorted set
        bucket_keys = [RRD_DATA_KEY(bucket, stat_field) for bucket in r.smembers(STAT_KEY + ':' + stat_field + ':buckets')]
        if bucket_keys == []:
            logger.error("No buckets for stat. Are you sure stat: %s exists?" % stat_field)
            return None
        r.zunionstore("tmpget", bucket_keys, aggregate='MAX')
        ts = [(tsdata.split(":")[0], int(tsdata.split(":")[1])) for tsdata in r.zrangebyscore("tmpget", start, end)]
        # In case there is no stats for start time or end time we prepend and append an non value
        # to the start and end so pandas has a full set of date and starts at start_date and end_date instead
        # of the first data with actual data and ending on the datetime with the last data
        ts.insert(0, (start, None))
        ts.append((end, None))
        # Create panda data frame for time series data
        df = pd.DataFrame(ts, columns=['Date', 'count'])
        # Convert epoch to datetime
        df.index = pd.to_datetime((df['Date']).astype(int), unit='s')
        # Convert to correct timezone
        df.index = df.index.tz_localize('UTC').tz_convert('Europe/London')
        # Resample for desired frequency
        df = df.resample(freq, how='last')
        # Create suitable labels
        if freq == 'min':
            format = '%d/%m/%Y %H:%-M'
        elif freq == 'M' or freq == 'BM' or freq == 'm':
            format = '%-m'
        else:
            format = '%d/%m/%Y %H:%-M'
        labels = []
        for label in df.index:
            str_label = label.strftime(format)
            if freq == 'M' or freq == 'BM' or freq == 'm':
                str_label = SHORT_MONTH_MAP[str_label]
            labels.append(str_label)
        df.index = labels
        return df

    def store(self, stat_field, count, increment=True):
        """ Updates Stat  (increment / replace)
            increment  if True adds count to current value stored at stat_field
                        else if False it replaces the current value
        """
        if increment:
            r.hincrby(STAT_KEY, stat_field, count)
        else:
            r.hset(STAT_KEY, stat_field, count)

    def initialise(self, stat_field):
        """ Initialise stat with default rrd buckets. """
        logger.info("Initialising %s with default buckets." % stat_field)
        # Set default value of zero for current value of stat
        r.hset(STAT_KEY, stat_field, 0)
        # Add stat to bucket's internal list of keys
        r.sadd(RRD_BUCKET_STATS_KEY('rrdbucket1'), stat_field)
        # Add bucket to stat own list i.e. should be sync'd to bucket's view
        r.sadd(RRD_STAT_BUCKETS_KEY(stat_field), 'rrdbucket1')

        r.sadd(RRD_BUCKET_STATS_KEY('rrdbucket2'), stat_field)
        r.sadd(RRD_STAT_BUCKETS_KEY(stat_field), 'rrdbucket2')

        r.sadd(RRD_BUCKET_STATS_KEY('rrdbucket3'), stat_field)
        r.sadd(RRD_STAT_BUCKETS_KEY(stat_field), 'rrdbucket3')

    def dump(self, *fields):
        """ Dumps Redis Stats """
        # If fields are not specified get all known stats
        if (fields == ()):
            fields = r.hkeys(STAT_KEY)
        for field in fields:
            logger.info(purple("Redis Dump of stat field: %s") % field)
            for bucket in r.smembers(RRD_STAT_BUCKETS_KEY(field)):
                data = r.zrange(RRD_DATA_KEY(bucket, field), 0, -1)
                logger.info(purple("bucket '%s' (length: %s)") % (bucket, len(data)))
                logger.info("%s" % data)

    def reset(self, delete_buckets=True, *fields):
        """ Clears stats. If fields is not specified all the stats will be cleared. """
        # If fields are not specified get all known stats
        if (fields == ()):
            fields = r.hkeys(STAT_KEY)
        # Clear current stat value
        r.hdel(STAT_KEY, *fields)
        # Delete all associated buckets?
        if delete_buckets:
            for field in fields:
                logger.info(purple("Deleting buckets of stat field: %s") % field)
                for bucket in r.smembers(RRD_STAT_BUCKETS_KEY(field)):
                    # Remove RRD data
                    r.zremrangebyrank(RRD_DATA_KEY(bucket, field), 0, -1)
                    # Remove bucket from stat's internal list
                    r.srem(RRD_STAT_BUCKETS_KEY(field), bucket)
                    # Delete stat from bucket's list / view of the world
                    r.srem(RRD_BUCKET_STATS_KEY(bucket), field)


# A list of buckets (bucketmanager)
# RRD_BUCKETS_KEY [bucket_name, bucket_name ....]  LIST


# Bucket config
# RRD_BUCKET_KEY:<bucket_name>  {'name', 'rows', 'steps', 'aggregation'}   HASH
# Stats in bucket
# RRD_BUCKET_KEY:<bucket_name> keys   [stat, stat, stat..] LIST

# Stat specific config for bucket
# RRD_BUCKET_KEY:<bucket_name>:<stat> {'full', 'current_row'}
# the rrd data
# RRD_BUCKET_KEY:<bucket_name>:<stat>:rrd     et('<timestamp>:<count>')

# ======================

# A list of buckets (redis-stat)
# STAT_KEY:<stat>:buckets [bucket_name, bucket_name ....]  set
# current value
# STAT_KEY <stat> <stat count>

#
#
#

if __name__ == '__main__':
        rs = redis_stat()
        rs.initialise('adas')
        rs.initialise('adas0')
        rs.store('adas', 10)
        rs.store('adas0', 2)
        rs.add_bucket('rrdbucket4', 'adas', 10, 2, 'average')
        
        #time.sleep(10)
        #rs.remove_bucket('adas', 'rrdbucket4')
        print "===="
        a = rs.get('adas', '3-11-2015 09:00:00', '03-11-2015 23:00:00', '5min')
        print "-------------"
        logger.info("%s" % a)

        #rs.dump('adas')


        ###rs.store('adas', 1, False)
        #print r.hgetall("redis-stat")
        #print r.hkeys("redis-stat")
        #rs.reset('adas')
        ####rs.reset()
        #print "after reset"
        #print r.hgetall("redis-stat")
