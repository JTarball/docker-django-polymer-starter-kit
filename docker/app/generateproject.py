#! /usr/bin/python
"""
    generate-project.py
    -------------------

    The purpose of this script to create the initial project setup.
    Scafffold out a template and do some basic check to ensure you are
     ready to go!

"""
import os
import subprocess
import sys
import psycopg2
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.base")
django.setup()

from django.contrib.auth.models import User


def generate_project():
    try:
        app_dir = os.environ.get('APP_DIR')
    except:
        sys.exit("The environment APP_DIR has not been set.")
    if app_dir is None:
        sys.exit("Environment variable APP_DIR is set to None. Not helpful! Please ensure it has been set")
    if os.listdir(app_dir) == []:
        subprocess.call(["cd %s && which yes > /dev/null; if [ $? -eq 0 ]; then yes | yo django-polymer; fi" % app_dir], shell=True)
        subprocess.call(["cd %s &&  which yes > /dev/null; if [ $? -eq 0 ]; then yes | npm install & bower install; fi" % app_dir], shell=True)
    else:
        sys.exit('App Directory: %s is not empty are you sure this is a new project?' % app_dir)


def create_superuser():
    """ Creates a Django superuser based on environment variables. """
    username = os.environ.get('SUPERUSER_NAME')
    password = os.environ.get('SUPERUSER_PASSWORD')
    email = os.environ.get('SUPERUSER_EMAIL')
    firstname = os.environ.get('SUPERUSER_FIRSTNAME')
    lastname = os.environ.get('SUPERUSER_LASTNAME')
    if None in (username, password, email, firstname, lastname):
        return sys.exit('Environment variables not set correctly for creating superuser.')
    u = django.contrib.auth.get_user_model().objects.create_superuser(username, email, password)
    u.first_name = firstname
    u.last_name = lastname
    u.is_superuser = True
    u.is_staff = True
    u.save()









def database_check():
    try:
        psycopg2.connect(
            dbname=os.environ.get('POSTGRES_NAME'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT'))
    except:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    generate_project()
    # log here - generated project template, now checking database environment variables
    database_check()


