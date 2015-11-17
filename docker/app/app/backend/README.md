<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>
## Yeoman generator for Django Polymer projects


## How to run 
We use docker and docker compose to run insolated development and production environments.

For more on docker compose: <a href="https://docs.docker.com/compose/" />

> If on a mac OSX ensure the docker daemon is up. e.g. `boot2docker up`

from root directory 
* `docker-compose up`
    will create the docker containers



### Docker Containers
 - docker-compose.yml    describes the container structure
    backend
    frontend
    postgres
    data - allows us to save the db and load on restart



### Daily Todo for completion of project 

# Backend
## Blog App
   - 















### What do you get 
- frontend
- backend
 The backend is powered by django and is specified used in that way i.e. it is only a backend and doesn't make use of any of django frontend templating etc. The django views are api only; to use you will need call via ajax (any other calls are banned).
 - - Django Apps
 - - - Accounts App
       - admin page for users (user profile edit/save/delete either)
       - admin page for superusers (stats)
       - admin page for staff  
       - staff admin for stats????
 - - - Blog App
 - - - Search Utility App
       Powered by redis you can perform lightning fast autocomplete/suggestions/search to point to specific 
 - - - Stats Utility App
       Powered by redis you can stat specific 
       - save stats per month for backups
       - uses rrd to keep values (round robin database) (last 18 months)

       included stats:
       - counter: registered users
       - counter: delete users
       - counter: current users
       - 

       - users logged in trend
       - searched words
       - blog page views


       - give data as json blob -> frontend graphs










# FUTURE WORK
 - - - Mailbot Django App
       - wrapper for mailchimp
       - default header
- - - Shop Django App



need to understand stats 
- counter or trend

- countter vs time series data

- counter is just counts so (just need reset really)
- time series (sampled data) -> round robin is needed


time series will not be decorators

 - bucket 1 function calculate stat (amount of users, page views etc.)



- how do the stats interact with the page; can we add stats to the page? how to do we display the data?


INFO APP ON INDEX.HTML SO IMPORTANT TO EXPLAIN FEATURES OF THIS APP!!!!!!!




TODO:
- DEFAULT DATA VIA FACTORIES
- TESTS -> REMEMBER HOW TO DO THEM AS WELL
- INFO PAGES ON HOW TO USE GENERATOR -- SO i DONT FORGET 
- useful dev tools - > model graphs --- should that be on the admin page (superuser) or just info page type graph.py etc.




- run scope of thsi project!!!




### regression tests for django can be called like so:






### Directory Structure

* __app/__

> this is created by __generator-polymer__ Do not move or rename to keep compatible with polymer generator commands

* __bower_components__

> this folder is also created by __generator-polymer__

* __apps/__

> Django apps folder

* __backend/__

> Django Project folder

* __tests/__

> Unit tests folder


### How to get started








<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>
## Yeoman generator for Django Polymer projects


## How to run 
We use docker and docker compose to run insolated development and production environments.

For more on docker compose: <a href="https://docs.docker.com/compose/" />

> If on a mac OSX ensure the docker daemon is up. e.g. `boot2docker up`

from root directory 
* `docker-compose up`
    will create the docker containers



### Docker Containers
 - docker-compose.yml    describes the container structure
    backend
    frontend
    postgres
    data - allows us to save the db and load on restart




NOTE: PYTEST IS USED FOR TESTING

### Directory Structure

* __app/__

> this is created by __generator-polymer__ Do not move or rename to keep compatible with polymer generator commands

* __bower_components__

> this folder is also created by __generator-polymer__

* __apps/__

> Django apps folder

* __backend/__

> Django Project folder

* __tests/__

> Unit tests folder


### How to get started


