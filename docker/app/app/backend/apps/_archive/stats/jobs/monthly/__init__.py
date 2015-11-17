"""
Daily cleanup job.

Can be run as a cronjob to clean out old data from the database (only expired
sessions at the moment).
"""

from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "Django Daily Cleanup Job"

    def execute(self):
        filename = "test.dat"     
        FILE = open(filename,"w")   
        print   "this is a test of a job"