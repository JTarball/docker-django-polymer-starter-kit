"""
    Utils.py
    Author: Danvir Guram
    Date: 12/11/11
    Utility functions for adding to Redis search
"""
import logging

from redis import Redis

from django.db import models
from django.core.urlresolvers import reverse

from project.utils.colours import green, sgreen, purple

# Get an instance of a logger
logger = logging.getLogger('project_logger')
# Connect to Redis
r = Redis()
# Redis Keys
ZKEY_AUTOCOMPLETE = 'autocomplete'
# WARNING: can't use ':' in key will generate ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
SKEY_DOCS_PREFIX = 'prefixs-'
SKEY_MODELS = 'models-'
SEARCH_RANKING = 'search-ranking-'


# Useful Notes on usage:
# zadd - sorted set
# sadd - set


# Here we have two sorted sets  - autocomplete of words and autocomplete of phrases

# Add Utilities use decorator
#
# View All Keys Stored for App
#
def log_dump_redis():
    """ Dump All Redis Data for Search App."""
    logger.info(sgreen('########################## REDIS DUMP FOR SEARCH APP ################################'))
    dumpStr = '\n###### Autocomplete ######\n'
    dumpStr += purple("%s") % r.zrange(ZKEY_AUTOCOMPLETE, 0, -1)  # Return a range of members in a sorted set, by index
    dumpStr += "\n###### Any Prefixs with key '%s' ######" % SKEY_DOCS_PREFIX
    for key in r.keys(SKEY_DOCS_PREFIX+'*'):
        dumpStr += green('\nKey: %s\n\t%s' % (key, r.sunion(key)))
        set_value = r.sunion(key)
        for redis_value in set_value:
            dumpStr += "\nKey: %s\n\t%s" %(SKEY_MODELS + redis_value, r.sunion(SKEY_MODELS + redis_value))

    logger.info(dumpStr)

    logger.info("For Prefix Key: '%s' Redis has the following keys:\n%s" % (SKEY_DOCS_PREFIX, r.keys(SKEY_DOCS_PREFIX+'*')))
    logger.info('############################## END OF REDIS DUMP ####################################')

def flush_redis():
    logger.info("Deleting all Redis keys: '%s'" % ZKEY_AUTOCOMPLETE)
    r.flushdb()

# --------------------- #
# Add Utility           #
# --------------------- #
# 
# Explain how it works:
# 
# set - just stores model and ids for fast search
# 
# 
# if result is only one -> go straight result page (so post)
# 
def add_model_to_redis_search(instance, **kwargs):
    def _add_phrase(phrase):
        phrase = phrase.strip().lower()  # strip empty leading or trailing space and lower caps
        if not phrase: logger.warning('There is a field in searchable_fields which is empty.')
        logger.info('Attempting to index the phrase: %s' % phrase)
        # Add all prefixs each word, and finally the word
        # Add complete phrase also 
        # add model reference to complete word or phrases in different key table 
        for word in phrase.split():
            for index in range(1, len(word) + 1):
                prefix = word[:index]
                logger.debug('adding prefix %s to key: %s' % (prefix, ZKEY_AUTOCOMPLETE))
                r.zadd(ZKEY_AUTOCOMPLETE, prefix, 0)                                       # adds prefixes e.g. (yield - y yi yie yiel yield)
            logger.debug('adding complete word: %s to key: %s' % (word + '*', ZKEY_AUTOCOMPLETE))
            r.zadd(ZKEY_AUTOCOMPLETE, word + '*', 0)#, 0)                                  # add the actual word (* denotes an actual word in redis search)
            logger.debug('adding %s to key: %s' % ((instance._meta, instance.pk), SKEY_DOCS_PREFIX))
            r.sadd(SKEY_DOCS_PREFIX + str(word), "%s:%s" % (instance._meta, instance.pk))  # autocomplete for phrase
        logger.debug('adding complete phrase: %s to key: %s' % (phrase + '*', ZKEY_AUTOCOMPLETE))
        r.zadd(ZKEY_AUTOCOMPLETE, phrase + '*', 0)                                         # add whole text
        logger.debug("adding whole phrase '%s:%s'" % ((instance._meta, instance.pk), 0))
        r.sadd(SKEY_DOCS_PREFIX + str(phrase), "%s:%s" % (instance._meta, instance.pk))    # add whole phrase
        if hasattr(instance, 'redis_stored_fields'):
            if all(hasattr(instance, attr) for attr in instance.redis_stored_fields):
                for field in instance.redis_stored_fields:
                    fieldVal = getattr(instance, field, None)
                    if hasattr(fieldVal, '__call__'): fieldVal = fieldVal()
                    logger.info("field %s in 'redis_stored_fields' of %s has val %s" % (field, instance, fieldVal))
                    if fieldVal is not None:
                        r.sadd(SKEY_MODELS + "%s:%s" % (instance._meta, instance.pk), "%s:%s" % (field, fieldVal))
            else:
                logger.error('Some fields in redis_stored_fields are not present in %s. Please recheck' % instance)

    logger.info('add_model_to_redis_search, model %s with id %s for searchable_fields %s' % (instance, instance.pk, instance.searchable_fields))
    if all(hasattr(instance, attr) for attr in instance.searchable_fields):
        for field in instance.searchable_fields:
            fieldVal = getattr(instance, field, '')
            # If fieldVal is manager add every object's name 
            if getattr(fieldVal, 'get_queryset', None) or getattr(fieldVal, 'get_query_set', None):
                for obj in fieldVal.all():
                    if not hasattr(obj, "name"): # TODO: inefficient to check everytime
                        logger.error("Object %s does not have a 'name' property" % obj)
                    else:
                        _add_phrase(obj.name)
            else:
                _add_phrase(fieldVal)
    else:
        logger.error('Some fields in searchable_fields are not present in %s. Please recheck' % instance)
        logger.error('Not added to Redis')


def addModelToRedis(phrase, model, pk):
    """ Adds to redis.
    where:
        model is the Django Model.
        pk is the primary key for the model (often the id).
    """
    phrase = phrase.strip().lower()  # strip empty leading or trailing space and lower caps
    if not phrase:
        raise ValueError("String is empty")

    for word in phrase.split():
        for index in range(1, len(word) + 1):
            prefix = word[:index]
            ###r.zadd(ZKEY_AUTOCOMPLETE, prefix)#, 0)  # adds prefixes e.g. (yield - y yi yie yiel yield)

        ###r.zadd(ZKEY_AUTOCOMPLETE, word + '*')#, 0)  # add the actual word (* denotes an actual word in redis search)
        ###r.zadd(SKEY_DOCS_PREFIX + word, "%s:%s" % (model, pk))  # autocomplete for phrase

    #r.zadd(ZKEY_AUTOCOMPLETE, phrase + '*', 0)                # add whole text
    ###r.zadd(SKEY_DOCS_PREFIX + phrase, "%s:%s" % (model, pk))  # add whole phrase
    logger.info("Added '%s' to redis search from database model: %s id: %s." % (phrase, model, pk))


# ---------------------- #
# Main Search Function  [Needs to be Fast!]
# ---------------------- #
def searchRedis(query, no_of_results=10):
    """Main Search Algorithm."""
    logger.info("Query entered: %s and we want %s results." % (query, no_of_results))
    if query is None:
        return []
    return [_model_from_redis(result) for result in autocompletePhrase(r, query, no_of_results)]


def custom_search_suggestion(word):
    """ """
    logger.info('%s' % word)


def autocomplete_suggestions(query, no_of_results=10):
    """ Create a serializable no. of suggestions. """
    logger.info("Autocompleting query: %s" % query)
    results = set()  # create (unique) set
    words = query.lower().split()
    # find all autocompletes for words in phrase or prefix
    [results.update(_autocomplete_word(r, word)) for word in words]
    best_guess_answer(results)
    # for every autocomplete produce some useful info for the frontend
    return [{'name': result, 'url': reverse('search:results')+ "?q=" + result, 'info': 'search'} for result in results]



def best_guess_answer(words, no_of_answers=3):
    """ Find the best answers from autocompletes 'words' - It is assumed words is correct """
    keys = [SKEY_DOCS_PREFIX+word for word in words]
    
    keys.extend(['%s' % SEARCH_RANKING])
    logger.info('best_guess_answer, keys: %s' % keys)
    logger.info(purple("%s") % r.zrange('tmp-df', 0, -1))
    try:
        r.zinterstore('tmp-df', keys)
        logger.info(purple("%s") % r.zrange('tmp-df', 0, -1))
    except:
        print "except"
    #[:no_of_answers]


def search_redis(query, no_of_counts=50):
    """ Search Redis for results of a search based on a query and returns a list of results
        # TODO: sort by some special parameter.
        # NOTE: only single query allowed
    """
    # Increment Ranking for this type of query; To increase best guess answer 
    r.zincrby(SEARCH_RANKING, SKEY_DOCS_PREFIX + query, 1)
    return sorted(r.sunion(SKEY_DOCS_PREFIX+ query), key=str.lower)[:no_of_counts]


def _convert_redis_to_key_value():

    pass


def create_context_from_search_results(search_results):
    """ Used with 
        TODO: stop user from giving bad formed
              separate this utility from app like blog
              optimise code
    """
    def create_json_data(key):
        content, id = key.split(':')
        app, model = content.split('.')
        logger.info("%s model" % r.sunion(SKEY_MODELS + key))

        model_fields = dict()
        for val in r.sunion(SKEY_MODELS + key):
            model_fields[val.split(':')[0]] = val.split(':')[1]

        logger.info('model_redis_fields: %s' % model_fields)
        if app == 'blog' and model == 'post':
            return {'name': model_fields['title'], 'url': model_fields['get_absolute_url'], 'info': 'Post'}
        elif app == 'blog' and model == 'postnode':
            return {'name': model_fields['name'], 'url': model_fields['get_absolute_url'], 'info': 'Section'}

    return [create_json_data(result) for result in search_results]
    # Can't think of a way of separating this at the moment
    

    # get attributes from models
    #[{'name': r.sunion(SKEY_MODELS + result)['title'], 'url': r.sunion(SKEY_MODELS + result), 'info': r.sunion(SKEY_MODELS + result)[]}  for result in search_results]


# name # Post in Section | Section | Search # uRL 


# go to straight to post
# 
# 
# Create sorted set of scores 
# - everytime a search is clicked increment score by 1
# - click on a result increment by 2 
# - then create a temporary sorted set? of only ones found
# 
# 
# need to change flush to keys and then delete on prefixes
# 
# 
# 
# search 
# go to section
# 
# 
# 
# normal suggestion search
# (name  then search/q?=name) json





# show first three as not search but straight to answer
# 
# Problems: how to determine best result
# increase 



def search_results_url():
    """ Helper function that takes key get results. If results produce only one answer """
    pass



def autocompletePhrase(r, phrase, count):
    """ Completes Phrase from stored Redis Phrases. """
    logger.info("Autocompleting Phrase: %s" % phrase)
    results = set()  # create (unique) set
    words = phrase.lower().split()
    logger.info("Split Phrase: [ %s ] into [ %s ]" % (phrase, words))
    [results.update(_autocomplete_word(r, word)) for word in words]

    keys = map(lambda k: SKEY_DOCS_PREFIX+k, results)
    logger.info("%s  results: %s" % (keys, results))
    if keys:
        return sorted(r.sunion(keys), key=str.lower)[:count]
    else:
        return []


def _autocomplete_word(r, word, count=10,  rangelen=50):
    """ Autocomplete a word. """
    results = set()
    logger.info("word: [ %s ]" % word)
    if not word:
        return results
    start = r.zrank(ZKEY_AUTOCOMPLETE, word)  # Determines the index of a member in a sorted set
    if not start:
        return results
    while len(results) <= count:
        entries = r.zrange(ZKEY_AUTOCOMPLETE, start, start + rangelen - 1)  # Return a range of members in a sorted set, by index
        logger.info("entries:\n%s" % entries)
        if not entries or len(entries) == 0:
            break
        start += rangelen

        for entry in entries:
            minlen = min((len(entry), len(word)))
            if entry[:minlen] != word[:minlen]:
                return results   # Is this correct

            if entry[-1] == '*' and len(results) <= count:
                results.add(entry[0:-1])
    return results


def _model_from_redis(redis_value):
    content, id = redis_value.split(':')
    app, model = content.split('.')
    model = models.get_model(app, model)
    return model.objects.get(id=id)
