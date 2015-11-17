#!/usr/bin/env python
"""
    stats.bucketmanager.py
    ======================


"""
# need to create a bucket service - bucket like server
# redis stat checks can connect on init
# adding to bucket - just adds key to keys (that should be saved in redis for persistence)
# bucketmanager

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
import random

import schedule

from datetime import datetime

from django.conf import settings

from redis import Redis


import logging


from project.utils.logger import DjangoProjectLogFormatter
from project.utils.colours import green, sgreen, purple

handler = logging.FileHandler(settings.SITE_ROOT + '/log/' + 'bucketmanager' + '.log',)
handler.setFormatter(DjangoProjectLogFormatter())

logger = logging.getLogger('bucketmanager')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



#REDIS_HOST = getattr(settings, "REDIS_HOST", '192.168.99.100')
REDIS_HOST = '192.168.99.100'

r = Redis(host=REDIS_HOST)
# Method of stat count calculation
METHOD_MAP = {"add": lambda n, m: n+m,
              "subtract": lambda n, m: n-m,
              "multiply": lambda n, m: n*m,
              "divide": lambda n, m: n/m,
              "average": lambda n, m: (n+m)/2
              }

BUCKETMANAGER_KEY = 'rrd-buckets'

BUCKET_CONFIG = {'name', 'rows', 'steps', 'aggregation'}
STAT_KEY = 'rrd-redis-stat'


BUCKET_DEBUG = True
if BUCKET_DEBUG:
    BUCKET1_INTERVAL = 1
    BUCKET1_ROWS = 5
else:
    BUCKET1_INTERVAL = 60
    BUCKET1_ROWS = 10080


# RRD_BUCKETS_KEY [bucket_name, bucket_name ....]  LIST
# RRD_BUCKET_KEY:<bucket_name>  {dictionray fo config including keys}   HASH
# RRD_BUCKET_KEY:<bucket_name>:<stat>   <timestamp:count> rank: integer defined by row  SORTED SET 

RRD_BUCKETS_KEY = BUCKETMANAGER_KEY + ':' + 'buckets'
RRD_BUCKET_KEY = BUCKETMANAGER_KEY + ':' + 'bucket'

def RRD_BUCKET_CONFIG_KEY(bucket_name):
    return "%s:%s" % (RRD_BUCKET_KEY, bucket_name)


def RRD_BUCKET_STATS_KEY(bucket_name):
    return "%s:%s:keys" % (RRD_BUCKET_KEY, bucket_name)

def RRD_DATA_KEY(bucket_name, stat_name):
    return "%s:%s:rrd" % (bucket_name, stat_name)

class Bucket:
    """
        Round robin database bucket.
        Acts like a circular buffer

        rows  - amount of measurements to store, the timespan in seconds of the native resolution equals to :steps*:rows
                "the number of rows in the circular buffer"
        steps - the interval in seconds in which to store measurements
                "the time interval between data(rows) in the circular buffer"
        aggregation - the method of aggregation
           options: 'sum'
    """

    def __init__(self, name, rows, steps, stat_keys, aggregation='sum'):
        self.name = name
        self.rows = int(rows)
        self.steps = int(steps)
        self.aggregation = aggregation
        if not isinstance(stat_keys, list):
            logger.error("The stat_keys must be a List type.")
            pass
        self.stat_keys = stat_keys
        self.job = None
        self.start()

    def start(self):
        """ Start Bucket RRD - scheduled sampling and consolidation. """
        self.job = schedule.every(self.steps).seconds.do(self._runScheduledTask)
        logger.debug("Starting RRD Bucket with a step of %s seconds." % self.steps)

    def clear(self):
        schedule.cancel_job(self.job)
        config = r.hgetall(RRD_BUCKET_KEY+':' + self.name)
        stat_keys = r.smembers(RRD_BUCKET_KEY + ':' + 'rrdbucket1' + ':' + 'keys')
        # Remove Stats info associated with this bucket
        fields = {'full', 'current_row'}
        for stat in stat_keys:
            r.hdel(RRD_BUCKET_KEY + ':' + self.name + ':' + stat, *fields)

        fields = {'name', 'rows', 'steps', 'aggregation'}
        r.hdel(RRD_BUCKET_KEY + ':' + self.name, *fields)
        r.hdel(RRD_BUCKET_KEY + ':' + self.name, '*')
        r.zremrangebyrank(RRD_BUCKET_KEY + ':' + self.name + ':' + 'rrd', 0, -1)
        r.delete(RRD_BUCKET_KEY + ':' + self.name + ':' + 'keys')

    def stop(self):
        schedule.cancel_job(self.job)

    def _runScheduledTask(self):
        """ Process new stat value A
            Add new value into buffer. If full need to consolidate values first. """
        logger.info("%s" % purple("="*100))
        logger.info('This is a schedule run task for bucket: %s for keys: %s' % (purple(self.name), self.stat_keys))
        for key in self.stat_keys:
            config = r.hgetall(RRD_BUCKET_KEY + ':' + self.name + ':' + key)
            count = r.hget(STAT_KEY, key)
            #current_row = int(config['current_row'])
            #full = int(config['full'])
            #count = config['count']
            #logger.debug("stat '%s' is on row %s  (full: %s, count: %s len of rrd: %s)" % 
            #              (key, current_row, full, count, len(r.zrange("%s:%s:rrd" % (self.name, key), 0, -1))))

            rrd_data = r.zrange("%s:%s:rrd" % (self.name, key), 0, -1)
            logger.error("ZRANGE 0 -1     %s" % rrd_data)
            logger.warn("ZRANGE -INF +INF %s" % r.zrangebyscore("%s:%s:rrd" % (self.name, key), float("-inf"), float("inf")))
            length_rrd = len(rrd_data)

            if (length_rrd == self.rows):
                timestamp = int(time.time())
                r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp, count), timestamp)
                logger.info("zrange 0 1 %s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, 1))
                data1, data2 = r.zrange("%s:%s:rrd" % (self.name, key), 0, 1)
                r.zremrangebyrank("%s:%s:rrd" % (self.name, key), 0, 1)
                timestamp_consolidated, data_consolidated = self.aggregrate(data1, data2)
                r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp_consolidated, data_consolidated), timestamp_consolidated)
                logger.debug("%s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, -1))  
            elif length_rrd > self.rows:
                logger.error("Length of RRD data %s (%s) is greater than bucket size %s. This should never happen. Removing excess data ..." % (self.name, length_rrd, self.rows))
                r.zrangebyscore("%s:%s:rrd" % (self.name, key), 0, (length_rrd - self.rows - 1))
            else:
                ## TODO: REMVOE LINE
                #count = random.randint(0, 10)
                # If buffer is not full, add new stat value and rotate circular buffer (increment current row)
                timestamp = int(time.time())
                r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp, count), timestamp)
                # Check full, increment current row & save to redis
                #if current_row == self.rows - 1:
                #    r.hmset(RRD_BUCKET_KEY + ':' + self.name + ':' + key, {'full': 1})
                #    current_row = 0
                #else:
                #    current_row += 1
                #r.hmset(RRD_BUCKET_KEY + ':' + self.name + ':' + key, {'current_row': current_row})
                logger.info("%s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, -1))

            # # If circular buffer (rrd) is full we need to consolidate/aggregrate
            # # else shift and add to sorted set
            # if full:
            #     # # TODO: REMVOE LINE
            #     # count = random.randint(0, 10)
            #     timestamp = time.time()
            #     r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp, count), timestamp)
            #     logger.info("zrange 0 1 %s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, 1))
            #     data1, data2 = r.zrange("%s:%s:rrd" % (self.name, key), 0, 1)
            #     r.zremrangebyrank("%s:%s:rrd" % (self.name, key), 0, 1)
            #     timestamp_consolidated, data_consolidated = self.aggregrate(data1, data2)
            #     r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp_consolidated, data_consolidated), timestamp_consolidated)
            #     logger.debug("%s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, -1))
            # else:
            #     ## TODO: REMVOE LINE
            #     #count = random.randint(0, 10)
            #     # If buffer is not full, add new stat value and rotate circular buffer (increment current row)
            #     timestamp = time.time()
            #     r.zadd("%s:%s:rrd" % (self.name, key), "%s:%s" % (timestamp, count), timestamp)
            #     # Check full, increment current row & save to redis
            #     if current_row == self.rows - 1:
            #         r.hmset(RRD_BUCKET_KEY + ':' + self.name + ':' + key, {'full': 1})
            #         current_row = 0
            #     else:
            #         current_row += 1
            #     r.hmset(RRD_BUCKET_KEY + ':' + self.name + ':' + key, {'current_row': current_row})
            #     logger.info("%s" % r.zrange("%s:%s:rrd" % (self.name, key), 0, -1))
        logger.info("%s" % purple("="*100))

    def dump(self):
        logger.info("%s" % r.hgetall(RRD_BUCKET_KEY + ':' + self.name))

    def aggregrate(self, data_1, data_2):
        timestamp_1, count_1 = data_1.split(":")
        timestamp_2, count_2 = data_2.split(":")
        logger.info("%s %s" % (count_1, count_2))
        count = METHOD_MAP[self.aggregation](float(count_1), float(count_2))
        logger.info("%s %s" % (timestamp_2, count))
        # Return most recent timestamp of two and aggregrated val
        return timestamp_2, int(count)#format(count, '.2f')


class BucketManager(object):
    """ BucketManager is a manager class for rrd buckets
        - that monitors changes in bucket config and buckets (on redis server)
        - keeps buckets alive to consolidate (rrd)
    """

    def __init__(self):
        self.delete_bucket('rrdbucket1')
        self.delete_bucket('rrdbucket2')
        self.delete_bucket('rrdbucket3')
        self.delete_bucket('rrdbucket4')


        self.buckets = []
        # Create default buckets if NO Redis data exists, else restore redis server state
        if (len(r.smembers(RRD_BUCKETS_KEY)) == 0):
            logger.info("creating default buckets")
            r.hmset(RRD_BUCKET_KEY + ':' + 'rrdbucket1', {'name': 'rrdbucket1', 'rows': BUCKET1_ROWS, 'steps': 10,
                                                     'aggregation': 'average', 'count': 0, 'current_row': 0, 'full': 0})
            r.sadd(RRD_BUCKET_KEY + ':' + 'rrdbucket1' + ':' + 'keys', 'user_logged_in')
            r.sadd(RRD_BUCKET_KEY + ':' + 'rrdbucket1' + ':' + 'keys', 'gays')

            r.hmset(RRD_BUCKET_KEY + ':' + 'rrdbucket1' + ':' + 'user_logged_in', {'current_row': 0, 'full': 0})
            r.hmset(RRD_BUCKET_KEY + ':' + 'rrdbucket1' + ':' + 'gays', {'current_row': 0, 'full': 0})
            r.hset(STAT_KEY, 'user_logged_in', 0)
            r.hset(STAT_KEY, 'gays', 0)

            r.hmset(RRD_BUCKET_KEY + ':' + 'rrdbucket2', {'name': 'rrdbucket2', 'rows': BUCKET1_ROWS, 'steps': 10*3,
                                                     'aggregation': 'average', 'count': 0, 'current_row': 0, 'full': 0})
            r.hmset(RRD_BUCKET_KEY + ':' + 'rrdbucket3', {'name': 'rrdbucket3', 'rows': 8760, 'steps': 10*5,
                                                     'aggregation': 'average', 'count': 0, 'current_row': 0, 'full': 0})
            # Create default buckets
            self.add_bucket('rrdbucket1', 10080, BUCKET1_INTERVAL, ['user_logged_in', 'gays'], 'average')     # 1 week at 1 min interval
            self.add_bucket('rrdbucket2', 10080, BUCKET1_INTERVAL*15, [''], 'average')  # 1 month at 15 min interval
            self.add_bucket('rrdbucket3', 8760, BUCKET1_INTERVAL*60, [''], 'average')   # 1 year (365 days) at 1 hour interval
        else:
            logger.info("restoring buckets")
            self.buckets = r.smembers(RRD_BUCKETS_KEY)
            logger.info("%s" % type(self.buckets))

        # Check for changes every 5 minute
        schedule.every(BUCKET1_INTERVAL).seconds.do(self.check_redis_buckets)
        schedule.every(BUCKET1_INTERVAL).seconds.do(self.check_redis_bucket_config)

        self.check_redis_bucket_config()
        self.check_redis_buckets()

        # Run Main Script
        self.run()

    def check_redis_bucket_config(self):
        """ Check Redis Bucket Config - for changes. """
        logger.debug('')
        logger.info("%s" % self.buckets)
        for bucket in self.buckets:
            logger.info("%s %s" % (bucket, type(bucket)))
            # If you change the name of the bucket in redis
            # it is assumed to be a new bucket - delete new cycle
            # i.e. name should is unique (NOTE: There is no protection for this at the moment)
            config = r.hgetall(RRD_BUCKET_KEY + ':' + bucket.name)
            stat_keys = r.smembers(RRD_BUCKET_KEY + ':' + bucket.name + ':' + 'keys')
            if str(bucket.rows) != config['rows']:
                print "rows have changed config, %s %s" % (bucket.rows, config['rows'])
                bucket.rows = int(config['rows'])
            if str(bucket.steps) != config['steps']:
                print "steps have changed config"
                bucket.steps = int(config['steps'])
            if str(bucket.aggregation) != config['aggregation']:
                print "aggregation has changed config"
                bucket.aggregation = config['aggregation']
            if bucket.stat_keys != stat_keys:
                logger.info("keys have changed config : %s  %s" % (bucket.stat_keys, stat_keys))
                bucket.stat_keys = stat_keys
                # Define Stat Config if no set yet
                for stat_key in bucket.stat_keys:
                    r.hsetnx(RRD_BUCKET_KEY + ':' + bucket.name + ':' + stat_key, 'current_row', 0)
                    r.hsetnx(RRD_BUCKET_KEY + ':' + bucket.name + ':' + stat_key, 'full', 0)

    def check_redis_buckets(self):
        logger.error('')
        if (len(self.buckets) != len(r.smembers(RRD_BUCKETS_KEY))):
            buckets = set([bucket.name for bucket in self.buckets])
            if len(r.smembers(RRD_BUCKETS_KEY)) > len(self.buckets):
                diff_buckets = r.smembers(RRD_BUCKETS_KEY) - buckets
            elif len(r.smembers(RRD_BUCKETS_KEY)) < len(self.buckets):
                diff_buckets = buckets - r.smembers(RRD_BUCKETS_KEY)
            else:
                print "error: this shouldnt happen. (changes during call?)"
                return

            print "diff_buckets: %s" % diff_buckets
            # Scan difference if in redis need to add to self.buckets and instantiate
            for diff_bucket in diff_buckets:
                if diff_bucket in r.smembers(RRD_BUCKETS_KEY):
                    config = r.hgetall(RRD_BUCKET_KEY+':'+diff_bucket)
                    stat_keys = r.smembers(RRD_BUCKET_KEY + ':' + config['name'] + ':' + 'keys')
                    print "config for stat keys: %s" % stat_keys
                    stat_keys1 = r.smembers(RRD_BUCKET_KEY + ':' + 'sadas' + ':' + 'keys')
                    logger.error("config for stat keys: %s" % stat_keys1)

                    print "config", config
                    if config != {} and config.has_key('name') and config.has_key('rows') and config.has_key('steps') and config.has_key('aggregation'):
                        # New bucket - create
                        print "new bucket"
                        self.add_bucket(config['name'], config['rows'], config['steps'], stat_keys, config['aggregation'])
                elif diff_bucket in buckets:
                    print "remove_bucket before call"
                    # No longer need this bucket - delete
                    self.remove_bucket(diff_bucket)

    def add_bucket(self, stat_field, rows, steps, keys, aggregation='average'):
        logger.info('Adding bucket with %s %s %s %s %s' % (stat_field, rows, steps, keys, aggregation))
        self.buckets.append(Bucket(stat_field, rows, steps, keys, aggregation))
        r.sadd(RRD_BUCKETS_KEY, stat_field)

    def remove_bucket(self, stat_field):
        rmbucket = [bucket for bucket in self.buckets if bucket.name == stat_field]
        if (len(rmbucket) != 0):
            for bucket in rmbucket:
                # Clear bucket stats from Redis
                # Remove buckets reference from Redis Remove bucket config
                # Remove from buckets array
                bucket.clear()
                self.buckets.remove(bucket.name)
                r.srem(RRD_BUCKETS_KEY, bucket.name)
        else:
            logger.error("Failed to remove bucket with name %s. It doesn't seem to exist." % stat_field)

    def delete_bucket(self, bucket_name):
        # Delete from list of known Buckets
        r.srem(RRD_BUCKETS_KEY, bucket_name)
        # Delete bucket config
        fields = {'name', 'rows', 'steps', 'aggregation'}
        r.hdel(RRD_BUCKET_CONFIG_KEY(bucket_name), *fields)
        # Delete All RRD stat data for this bucket
        [r.zremrangebyrank(key, 0, -1) for key in r.keys(RRD_DATA_KEY(bucket_name, "*"))]
        # Delete stats list associated to bucket
        r.delete(RRD_BUCKET_STATS_KEY(bucket_name))

    def dump(self):
        """ Dumps all Redis stored information. """
        logger.info("%s" % r.smembers(RRD_BUCKETS_KEY))
        for bucket in self.buckets:
            bucket.dump()

    def run(self):
        """ Main run script. """
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
        #keys = r.keys("rrdbucket4:*:rrd")
        #[r.zremrangebyrank(key, 0, -1) for key in r.keys("rrdbucket4:*:rrd")]
        #r.zremrangebyrank('rrdbucket1' + ':' + 'user_logged_in' + ':' + 'rrd', 0, -1)
        #r.zremrangebyrank('rrdbucket1' + ':' + 'gays' + ':' + 'rrd', 0, -1)
        rs = BucketManager()
