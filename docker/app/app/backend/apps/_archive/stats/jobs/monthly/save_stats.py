import logging
import time    
from django_extensions.management.jobs import MonthlyJob
from redis import Redis
from datetime import datetime
logger = logging.getLogger(__name__)
r_server = Redis()

class Job(MonthlyJob):
    help = "Storing monthly stats."

    def execute(self):
        logger.info('Saving stats...')
        dt = datetime.now()
        dump_filename = "%s_%s_dump.rdb" % (dt.month, dt.year) 
        r_server.config_set('dbfilename', '%s' %dump_filename)
        logger.info("Set dbfilename: %s" % (r_server.config_get('dbfilename')))
        r_server.bgsave()
        time.sleep(10) # need to fix -- this is bad
        r_server.config_set('dbfilename', 'redis_primary_dump.rdb')
        logger.info('Clearing stats...')
        r_server.flush()
        
    
