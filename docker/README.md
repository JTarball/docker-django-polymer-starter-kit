<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>

## 'docker' Directory 

This contains all the files needed to create Docker Images for this project including any development files.

### Files

* **README.md**
  - this file
* **app/**
  - docker for app including development files for django and polymer 
  - derived from 'jtarball/docker-base' (automated build from docker hub)
  - your project directory is in here
* **base/**     
  - clone of 'docker-base' repo
  - docker files for base image
  - only included in case you need a custom base image else you can delete this folder
* **nginx/**      
  - docker files for nginx service 


### 'base' directory 
This is the base docker image - os with some extras provisioning for webapps. 
Note you should never just use this on its own as it is meant as a 'base' as 
such requires requirements etc.

### 'app' directory
This is the main docker image used for this project. This folder contains a directory 
which will contain all development files (django & polymer). This is shared for development.



