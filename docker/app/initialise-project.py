#! /usr/bin/python
"""
    generate-project.py
    -------------------

    The purpose of this script to create the initial project setup.
    Scafffold out a template and do some basic check to ensure you are
     ready to go!

     THIS MAY NOT WORK!!!!!!!!!!!!!!!!

"""
import os
import subprocess
import sys
import psycopg2

try:
    app_dir = os.environ.get('APP_DIR')
except:
    sys.exit("The environment APP_DIR has not been set.")

sys.path.append(app_dir + '/backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.base")
from django.contrib.auth.models import User


def initalise_project():
    try:
        app_dir = os.environ.get('APP_DIR')
    except:
        sys.exit("The environment APP_DIR has not been set.")
    if app_dir is None:
        sys.exit("Environment variable APP_DIR is set to None. Not helpful! Please ensure it has been set")
    subprocess.call(["cd %s &&  which yes > /dev/null; if [ $? -eq 0 ]; then yes | npm install & bower install; fi" % app_dir], shell=True)


def create_superuser():
    username = os.environ.get('SUPERUSER_NAME')
    password = os.environ.get('SUPERUSER_PASSWORD')
    email = os.environ.get('SUPERUSER_EMAIL')
    if None in (username, password, email):
        return sys.exit('Environment variables not set correctly for creating superuser.')
    u = User(username=username)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()


def database_check():
    try:
        psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
    except:
        return sys.exit('Could NOT connect successfully to postgres - check environment variables.')

    sys.exit(0)

if __name__ == "__main__":
    initialise_project()
    create_superuser()
    database_check()