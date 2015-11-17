#!/usr/bin/env python
"""
    stats.redis-stats.py
    ====================


"""

# For now using sorted set 
# technically list should be quicker 
# but having the set might be used when timestamp are involved




#zadd

# bucket-name-stat-name "<timesatmp>:count",   <row number>
# use row number as zrank to keep order



#addStatkey


# shift and aggregrate



import logging
import schedule
import time


logger = logging.getLogger('project_logger')

AGGREGRATION_MAP = {
    "sum": lambda n, m: n+m,
    "subtract": lambda n, m: n-m,
    "multiply": lambda n, m: n*m,
    "divide": lambda n, m: n/m,
    }


'<bucket-name>:<stat>, <timestamp:count>'

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

    def kill(self):
        pass

    def _runScheduledTask(self):
        """ Process new stat value A
            Add new value into buffer. If full need to consolidate values first. """
        print 'hdkjsahfdhsajkdsa'
        if self.full:
            r.zremrangebyrank("")
        else:
            # If buffer is not full, add new stat value and rotate circular buffer
            timestamp = '12131324213'
            count = 10
            key = 'fsdfs'
            r.zadd("%s-%s" % (self.name, key), "%s:%s" % (timestamp, count), self.current_row)
            self.current_row += 1

        for key in self.keys:
            print key


    def aggregrate(self, key):
        pass

    def addStatKey(self):
        pass

if __name__ == '__main__':
    b = Bucket()
    b.addStatKey()
    b.start()
    #b.stop()
    while 1:
        schedule.run_pending()
    #     time.sleep(1)
