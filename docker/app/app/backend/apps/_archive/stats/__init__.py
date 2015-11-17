


"""
example of how to add a stat using redis_stats app

@redis_stat.register(rate_limit='15/m')
def user_count():
    """"""How to update this stat""" """
   pass


create a stats.py in the app you want to update/ take stats from 

should also take care of trends  - for admin graphs
should take care of cron/celery  and redis 


stats are saved every month via cron






"""