[![Circle CI](https://circleci.com/gh/JTarball/docker-django-polymer-starter-kit.svg?style=svg)](https://circleci.com/gh/JTarball/docker-django-polymer-starter-kit)


<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>

<img src="https://www.polymer-project.org/images/logos/lockup.svg" />


#### Current Integrated Version/s 

-	[`v1.2.6`, `generator-polymer`](https://github.com/yeoman/generator-polymer.git)
-	[`1.8.6`, `Django`](https://www.djangoproject.com/download/)

## Django Polymer start project using Docker
## Intro
This is a quick fire starter kit for getting a Docker Web project up and running. Django web framework is used for the backend essentially making it a  REST API. Google Polymer is used for the frontend.

This project integrates **generator-polymer** project with a dockerized django app.

## Cheatsheet
### Rebuild and Upload base image 


### Useful Commands
`docker login`
  - you will need to login into docker hub (set up an account if you dont have one)
`docker build -t "<IMAGE>" .`
  - this will build the Dockerfile in the current directory and tag it with "jtarball/docker-base:latest"
`docker push "<IMAGE>"`
  - push to docker hub
`docker-compose up`
 - this command will create and start containers
`docker rm $(docker ps -a -q); docker rmi $(docker images -q);`
 - kill and remove all docker images and containers
`docker rmi $(docker images -q --filter "dangling=true")`
 - Ckean up un-tagged docker images




## How to use
1. Install Polymer FrontEnd Components
npm install -g gulp bower && npm install && bower install


### How to deploy to Amazon Web Services

To deploy this project to AWS you must set the following environment variables:

* DOCKERHUB_USER
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_VPC_ID

```
export DOCKERHUB_USER=jtarball
export AWS_ACCESS_KEY_ID=xxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxx
export AWS_VPC_ID=xxxx
```


 run `create-docker-machine-aws.sh  <MACHINE_NAME>` where MACHINE_NAME is the name for the machine you want created 
 run `python build-tag-push.py` which will build the docker app, push it to docker hub and a new compose yml file (you will need to be logged in  `docker login`)




## Directory Structure


## License

View [license information](https://github.com/JTarball/docker-base/blob/master/LICENSE) for the software contained in this image.

## User Feedback

Any feedback or comments  would be greatly appreciated: <james.tarball@gmail.com>

### Issues

If you have any problems with or questions about this image, please contact us through a [GitHub issue](https://github.com/JTarball/docker-base/issues).

You can also reach me by email. I would be happy to help  <james.tarball@gmail.com>

## Developer Notes
#### How to upgrade base directory
#### Considerations / Future Work














### Tutorial

* [Flux7's Dockerfile Tutorial](http://flux7.com/blogs/docker/docker-tutorial-series-part-3-automation-is-the-word-using-dockerfile/)

## Layers

The versioned filesystem in Docker is based on layers.  They're like [git commits or changesets for filesystems](https://docs.docker.com/terms/layer/).

Note that if you're using [aufs](https://en.wikipedia.org/wiki/Aufs) as your filesystem, Docker does not always remove data volumes containers layers when you delete a container!  See [PR 8484](https://github.com/docker/docker/pull/8484) for more details.

## Links

Links are how Docker containers talk to each other [through TCP/IP ports](https://docs.docker.com/userguide/dockerlinks/).  [Linking into Redis](https://docs.docker.com/examples/running_redis_service/) and [Atlassian](https://blogs.atlassian.com/2013/11/docker-all-the-things-at-atlassian-automation-and-wiring/) show worked examples.  You can also (in 0.11) resolve [links by hostname](https://docs.docker.com/userguide/dockerlinks/#updating-the-etchosts-file).

NOTE: If you want containers to ONLY communicate with each other through links, start the docker daemon with `-icc=false` to disable inter process communication.

If you have a container with the name CONTAINER (specified by `docker run --name CONTAINER`) and in the Dockerfile, it has an exposed port:

```
EXPOSE 1337
```




























# Todo

- create repo docker-base
- sublink to generator-dockerized django-polymer 
- add comments to explain


- need to separate 





# Docker Image
 > base 
  - this has been included if required custom modification (from docker-base in github)
  - has some dependencies when called (requirements etc)
  

 - app
  - derived from docker-base:latest from docker hub ( 'docker-base' automated build via docker hub to keep up to date )
  - requires manual build, tagging & deployment
  - why not automated build via docker hub ---- more flexibility without, need a different .yml for production etc.




# How to get started 


# Docker Images explained




# App Docker Image 
 - use a base image - dockerfile and stuff included in case you want to see - automated build so always latest
 - app  manual updates







Docker linguistics borrow from git terminology, but it’s rather dangerous to interpret these too literally.
Keeping a clean docker environment

run interactive containers with --rm flag to avoid having to remove them later.

Remove all stopped containers:

Clean up un-tagged docker images:
docker rmi $(docker images -q --filter "dangling=true")
Stop and remove all containers (including running containers!)
Docker and Continuous Integration



> docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q);
> 
> 
> 
> 
> 
> 
> 
> docker run -v /Users/danvir/Masterbox/sideprojects/github/docker-django-polymer/app_mount:/app -i -t dockerdjangopolymer_app_1


# Run tests on app
py.test --ds=project.settings.test  <app dir>
REUSE_DB=0 python manage.py test --settings=project.settings.test -s --with-queries blog


# AWS EB
https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/













[![NPM version](http://img.shields.io/npm/v/generator-django-polymer.svg?style=flat)](http://npmjs.org/generator-django-polymer)
[![NPM downloads](http://img.shields.io/npm/dm/generator-django-polymer.svg?style=flat)](http://npmjs.org/generator-django-polymer)
[![Build Status](http://img.shields.io/travis/JTarball/generator-django-polymer/master.svg?style=flat)](https://travis-ci.org/JTarball/generator-django-polymer)
[![Dependency Status](http://img.shields.io/david/JTarball/generator-django-polymer.svg?style=flat)](https://david-dm.org/JTarball/generator-django-polymer)



### Introduction to generator-django-polymer

Yeoman generator that scaffolds out a Django project with Polymer.

> This generator extends [generator-polymer](https://github.com/yeoman/generator-polymer) and integrates it with a Django project generator

### Why extend generator-polymer?

Google Polymer is an awesome framework leveraging the new standards of web components however 
it is still a relatively new framework.

As of yet it has even reached version 1.0 likely to change which will have a knock on effect to 
the best standards and practices for Polymer project layouts/scaffolds.

Thus this generator project will periodically integrate new changes from __generator-polymer__
to incorporate the latest changes, methods and best practices

This currently is a better solution than creating a rigid custom layout for a Polymer compatible app which may change.

### How is Django and Polymer integrated in this project?
This is likely to be the more important question when deciding whether to use this generator or not.

Main points:

* The output of **generator-polymer** is kept largerly intact. 
* We symbolic link all polymer elements to Django's static folder.
* Routing is still performed by Django's urls
* Django templating is still used but is minimally required with a project like this compared to a standard Django project. See generated output for example on use.
* Where conflicts exist in templating we use the __verbatim__ django tag.

Thus, we get a project that has all the benefits of a polymer frontend app as well as all the benefits of Django's backend environment including
urls, templating etc. without having to interleave both projects in a complex way.

*in theory, if you decided that Polymer was not for you; removing it without affecting the Django project should be easy.*


### Directory Structure
The settings files are split for better separate of roles:

* __README.md__

> this file

* __app/__

> this is created by __generator-polymer__ Do not move or rename to keep compatible with polymer generator commands

* __bower_components__

> this folder is also created by __generator-polymer__

* __apps/__

> Django apps folder

* __project/__

> Django Project folder

* __tests/__

> Unit tests folder

* __Gulpfile.js | Gruntfile.js | etc. 
...__

> optional files created by *generator-polymer* 







### Developer Notes

#### How to update base docker image 'docker-base'
From `docker` directory run:
```
git submodule update --remote --merge 
```

### Considerations / Future
In the future I might consider incorporating ideas from the following projects:

* https://github.com/imkevinxu/django-kevin
* https://github.com/luzfcb/cookiecutter-django-oauth
* https://github.com/pydanny/cookiecutter-django

*e.g. caching, sendGrid email support, heroku, better management*
