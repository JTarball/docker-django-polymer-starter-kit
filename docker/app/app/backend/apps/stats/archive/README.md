
- resolution
- range
- metric to query
- aggergaration method


REDIS_STAT_PREFIX='stats'


class Bucket:
	pass


# ok no definitons - just expect not to make mistake

# Stage One

# no config file, definition, no modification of buckets for stats other then 
# by function code


class RedisStats:

	def init():
		# reload redis stat db
		# create buckets 
		pass

	def addBucket():
		pass

	def get(, aggregation=None):
		pass

	def store():
		pass

	def dump(key=None, range=None):
		""" Dumps Redis Stats ""

	def reset():
		pass

	def clear(key, range):
		pass

logger = logging.getLogger('project_logger')

class Bucket:

	def init:
		self.rows = NA
		self.steps = NA
		self.aggregration = NA
		self.keys = # a list of keys for this bucket
		self.job = None

	def start(self):
		self.job = se
		schedule.every(self.steps).do(self._runScheduledTask())

	def stop(self):
		schedule.cancel_job

	def _runScheduledTask():
		logger.info('hdkjsahfdhsajkdsa')





:steps interval in seconds in which to store measurements

:rows amount of measurements to store, the timespan in seconds of the native resolution equals to :steps*:rows

:aggregations array of aggregations to use for this measurement, currently available: average, min, max, sum





import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)




10 10 10 10 10 10


 






- ok so ...


need buckets 
- 5min
- hr
- d
- w
- m


name: count

name:timestamp count


- how should the stat be updated or added with python code (decortora?)d
- hash for current count
- then buckets are sorted sets?

















could consist better granularity later



- turn data in 5 min frequency
- add to 5 min bucket

- cicrcular buffer

- 5min x 12 = 60min = 1hr
- 1hr x 24 = 1 day
- 1day x 7 = 1 week
- 1week x 4 = 1 m 

- 1m x 18 - 1year and half



- bucket one:

- every 5min - 12 x 24 x 7 = 2016   (1 week)
- every hr   - 24 x 7 x 4 = 672     (1 month)
- every day  - 500 days             
- every week - 52 x2  104
- every month -  12 x 5 = 60





- a bucket 
- has a consolidation function: average, last, min, max
- steps
- rows








need a get function





60x24x7



The get function takes three or four arguments:

The metric to query
Starting time stamp for the timespan to return
Ending time stamp for the timespan to return
Optional aggregation method
The array returned contains two arrays, the first one with unix timestamps of the measurements, the second one the (aggregated) values.

Configuration

Per default RReDis is configured to store one measurement every 10 seconds for one day (called native resolution from here on), and then aggregate the measurements for the following timespans:

1 week at 1 minute resolution
1 month at 15 minute resolution
1 year at 1 hour resolution





http://redis4you.com/articles.php?id=010


Redis save and backup script

This is idea how you can backup the file RDB file.

Basicaly you need to set up two crontab processes. First must perform BGSAVE:

redis-cli bgsave
When this is call, Redis will perform background save. Process usually will finish couple of minutes later. At the end new RDB file will be created.

Second crontab must start 10-15 min later. It needs to move / copy / upload the file to different location. For simplicity here I will simulate a copy to different disk or NFS image.

cp /data/redis/dump.rdb /backup/redis.dump.rdb
Here someone may rise very important question:
What will happen, if Redis begin to save at the time we copy?

Answer is trivial - if you are using modern filesystem, everything is OK and nothing will happen.

This is because of the way Redis do save operation.
First Redis forks, then it saves under temporary file. After process is done, Redis deletes the old file and rename temporary file.

In modern filesystems such EXT2, EXT3, XFS, RaiserFS, NTFS etc., the file always will be copied normally even file is deleted, because delete do not remove the file, but rather remove the only the link to the file. For more information, you may refer to UNIX C unlink() function.

How to do daily backup file

If we just copy the file, today's file will replace yesterday's. This is not always a good idea.

If we want to keep daily backup we can add "date '+%a'" and to append it to the backup filename. The following example also includes configurable directories.

REDIS_SOURCE=/data/redis/dump.rdb
BACKUP_DIR=/backup

BACKUP_PREFIX="redis.dump.rdb"
DAY=`date '+%a'`
REDIS_DEST="$BACKUP_DIR/$BACKUP_PREFIX.$DAY"

cp $REDIS_SOURCE $REDIS_DEST
Crontab set-up

For those who are not familiar with crontab, here you are the crontab script itself:

# Do BGSAVE
0  0 * * *	redis-cli bgsave

# Simple copy
15 0 * * *	cp /data/redis/dump.rdb /backup/redis.dump.rdb

# ... or call more complex script (example is commented)
#15 0 * * *	/scripts/perform_copy.sh