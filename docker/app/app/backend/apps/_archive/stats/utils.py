from datetime import datetime, timedelta
from redis import Redis
import subprocess
import time
import logging # import the logging library
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Initialise Redis server
r_server = Redis()


def load_redis_db(filename):
    """Loads database"""
    # copy 
    file1 = filename
    file2 = "./temp.rdb"
    conf = "./redis_secondary.conf"
    subprocess.call(["cp", file1,file2])
    subprocess.call(["./redis-server", "%s" %(conf)])
    # to connect need to use strictserver via python redis
    
    

