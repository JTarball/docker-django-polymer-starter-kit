"""
    decorator.py
    Author:    Danvir Guram
    Date:      20/10/11

Decorator Class for adding redis search indexing

"""
import logging

from django.db.utils import DatabaseError

from . import utils

# Get instance of logger
logger = logging.getLogger('project_logger')


class Redis_Search(object):
    """ Class to wrap add indexing a django model.
    django model MUST have an url / get_absolute_url needs a category
    """

    #def __init__(self, *args, **kwargs):
    #    logger.info('__init__')
        #self.index = []
        #for arg in args:
        #    logger.info("initialising model [ %s ]redis search: %s" % (self, arg))
        #    self.index.append(arg)

    def __call__(self, django_model=None):
        """ Gets all models and adds every index to redis search.
        This function will get called every syncdb.
        Clears and Updates everytime?
        """
        logger.info('__call__')
        try:
            models_data = django_model.objects.all()
            models_data.count()  # used to invoke DatabaseError if model doesnt exist
        except DatabaseError:
            logger.warning("No instances of model %s. I hope this is the first time u have run this for this model. Otherwises... " % django_model)
            logger.warning("Failed to add to Redis.")
            return django_model

        for model in models_data:

            #if not hasattr(model, "category"):
            #    raise Exception("Model %s must have category attribute for the Model to be indexed via Redis Search" % model)

            #if not(hasattr(model, 'get_absolute_url') or hasattr(model, "url")):
            #    raise Exception("Model %s must have url attribute or a get_absolute_url function for the Model to be indexed via Redis Search" % model)

            #for index in self.index:
            logger.info("Indexing attribute: %s of model: [ %s ] into Redis Search." % ("unknown", django_model))
                #utils.addModelToRedis(model.__getattribute__(index), model._meta, model.pk)
