#! /usr/bin/python
"""
    ci.py
    -------------------

    The purpose of this script to run as a regression
    script to test the project docker build.

"""
import os
import sys
import psycopg2




# Check admins as been created correctly
# Check redis is up
# Check database connect
# Check emails can be sent
# Django health check
# Check services
# Django system check
#check redis connection


def database_check():
    print "Checking Database setup - environment variables ..."
    try:
        psycopg2.connect(
            dbname=os.environ.get('POSTGRES_NAME'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'))
    except:
        print "fdsfsd"
        #sys.exit(1)

    #sys.exit(0)


if __name__ == "__main__":
    database_check()
    print "dsdfs"
