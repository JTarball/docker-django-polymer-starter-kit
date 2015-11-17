"""

    search.utils.py
    ===============

    This is the main file for adding Redis search
    capability to django models

    - support for Taggit (TaggableManager)

    How to use:


"""
import logging

import taggit
from redis import Redis

from project.utils.colours import green, sgreen, purple
from django.db import models
from django.conf import settings

REDIS_HOST = getattr(settings, "REDIS_HOST", None)

logger = logging.getLogger('project_logger')
# Connect to Redis
r = Redis(host=REDIS_HOST)
# Redis Keys
ZKEY_AUTOCOMPLETE = 'prefixes-'
ZKEY_AUTOCOMPLETE_SCORE = 'prefscores-'
# WARNING: can't use ':' in key will generate
# ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
SKEY_AUTOCOMPLETE = 'complete-'
SKEY_MODELS = 'models-'
ZKEY_TMP_SEARCH_RANKING = 'search-'


# =====================================================================
# Utility Functions for adding to redis, flushing redis and log dumping
# =====================================================================
def add_model_to_redis(instance, **kwargs):
    """
    Adds Django Model Fields to Redis Search.

        Adds a Django model fields to redis - caches for high speed search
        perfect for autocomplete

        Three sets are used for storage denoted by prefix ZKEY_AUTOCOMPLETE, SKEY_AUTOCOMPLETE, SKEY_MODELS
        ZKEY_AUTOCOMPLETE - for storing all prefixes of words
        ZKEY_AUTOCOMPLETE_SCORE - occurence for complete words in searchable_fields
        (<complete word/phrase>:<django_model_meta>:<django_pk>, <occurence_count_in_searchable_fields>)   (key, value)
        SKEY_AUTOCOMPLETE -  (<complete word/phrase>, <django_model_meta>:<django_pk>)   (key, value)
        SKEY_MODELS - (<django_model_meta>:<django_pk>, <django_field>:<django_field_value>)  (key, value)

        How works:
        All prefixes of words/phrases are stored in sorted set ZKEY_AUTOCOMPLETE. (y yi yie yiel)
        The complete words/phrases are stored in sorted set ZKEY_AUTOCOMPLETE denoted by *. (yield*)
        The complete words are used as key for SKEY_AUTOCOMPLETE set.
        The value of the key being <django_model_meta>:<django_pk>
        All 'redis_stored_fields' are stored in another set with the key <django_pk> (super fast cache)

        How to use:
        - add 'searchable_fields' to django model with the words you want to use when searching
        - add to 'redis_stored_fields' all the fields in the model you want cached in the redis store.
        - add a signal to reevaluate the redis store e.g. post_save

        Example:

        class Post(models.Model):
            searchable_fields = ['title']
            redis_stored_fields = ['title', 'slug', 'get_absolute_url']  # what fields should be cached
            title = models.CharField(max_length=255)
            ...

        def reindex_redis_search(sender, instance, **kwargs):
            logger.info("Re-creating Search Autocomplete Index ...")
            flush_redis()
            [add_model_to_redis_search(model) for model in Post.objects.all()]
            log_dump_redis()

        signals.post_save.connect(reindex_redis_search, sender=Post, dispatch_uid="add_post_tags")


        Here the redis store is reevaluated everytime the model is saved. The title of the Post model
         is used as a way of searching for a specific Post.  The title, slug and url would be used in the
         autocomplete of the search bar to link to a specific Post page.


        Two sets used:
        zadd - sorted set (for autcomplete of words/phrases)
        sadd - set (for referencing models)


    """
    def _add_phrase(phrase):
        """ """
        # Strip empty leading or trailing space and lower caps
        phrase = phrase.replace(".", " ")
        phrase = phrase.strip().lower()
        if not phrase:
            logger.warning('There is a field in searchable_fields which is empty.')
            return
        logger.info('Attempting to index the phrase: %s' % phrase)
        # Add all prefixs of each word, and then finally the word (to prefix ZKEY_AUTOCOMPLETE)
        # Add complete phrase (to prefix ZKEY_AUTOCOMPLETE)
        # Use complete words and phrases as key to reference Django Model  (to prefix SKEY_AUTOCOMPLETE)
        for word in phrase.split():
            for index in range(1, len(word) + 1):
                # adds prefixes e.g. (yield - y yi yie yiel yield)
                prefix = word[:index]
                logger.debug('adding prefix %s to key: %s' % (prefix, ZKEY_AUTOCOMPLETE))
                r.zadd(ZKEY_AUTOCOMPLETE, prefix, 0)
            logger.debug('adding complete word (denoted by *): %s to key: %s' % (word + '*', ZKEY_AUTOCOMPLETE))
            r.zadd(ZKEY_AUTOCOMPLETE, word + '*', 0)
            logger.debug('adding %s to key: %s' % ((instance._meta, instance.pk), SKEY_AUTOCOMPLETE))
            r.sadd(SKEY_AUTOCOMPLETE + str(word), "%s:%s" % (instance._meta, instance.pk))
            r.zincrby(ZKEY_AUTOCOMPLETE_SCORE, "%s:%s:%s" % (str(word), instance._meta, instance.pk), 1)
        logger.debug('adding complete phrase: %s to key: %s' % (phrase + '*', ZKEY_AUTOCOMPLETE))
        r.zadd(ZKEY_AUTOCOMPLETE, phrase + '*', 0)
        logger.debug("adding whole phrase '%s:%s'" % ((instance._meta, instance.pk), 0))
        r.sadd(SKEY_AUTOCOMPLETE + str(phrase), "%s:%s" % (instance._meta, instance.pk))
        r.zincrby(ZKEY_AUTOCOMPLETE_SCORE, "%s:%s:%s" % (str(phrase), instance._meta, instance.pk), 1)

        # Store (caches) 'important' fields so don't have to hit the database
        if hasattr(instance, 'redis_stored_fields'):
            if all(hasattr(instance, attr) for attr in instance.redis_stored_fields):
                for field in instance.redis_stored_fields:
                    fieldVal = getattr(instance, field, None)
                    if hasattr(fieldVal, '__call__'):
                        fieldVal = fieldVal()
                    logger.info("field %s in 'redis_stored_fields' of %s has val %s" % (field, instance, fieldVal))
                    if fieldVal is not None:
                        r.sadd(SKEY_MODELS + "%s:%s" % (instance._meta, instance.pk), "%s:%s" % (field, fieldVal))
            else:
                logger.error('Some fields in redis_stored_fields are not present in %s. Please recheck' % instance)

    if all(hasattr(instance, attr) for attr in instance.searchable_fields):
        for field in instance.searchable_fields:
            logger.debug("Model %s (%s) - %s" % (instance, instance.pk, field))
            fieldVal = getattr(instance, field, '')
            if isinstance(fieldVal, taggit.managers._TaggableManager):
                for str_tag in fieldVal.names():
                    _add_phrase(str_tag)
            else:
                _add_phrase(fieldVal)
    else:
        logger.error('Some fields in searchable_fields are not present in %s.\
                      Please recheck.\nNot Added to Redis.' % instance)


def dump_redis():
    """Dump all Redis data for Search App in the logger. """
    logger.info(sgreen('==================== REDIS DUMP FOR SEARCH APP ===================='))
    dumpStr = '\n===== Autocomplete =====\n'
    dumpStr += purple("%s\n") % r.zrange(ZKEY_AUTOCOMPLETE, 0, -1)  # Return a range of members in a sorted set
    dumpStr += '\n===== Complete words/phrase score based on autocomplete =====\n'
    dumpStr += purple("%s\n") % r.zrangebyscore(ZKEY_AUTOCOMPLETE_SCORE, float("-inf"), float("inf"))
    dumpStr += "\n===== Any Prefixs with key '%s' =====" % SKEY_AUTOCOMPLETE
    for key in r.keys(SKEY_AUTOCOMPLETE+'*'):
        dumpStr += green('\nKey: %s\nValue: %s\n' % (key, r.sunion(key)))
    dumpStr += "models:"
    for key in r.keys(SKEY_MODELS+"*"):
        dumpStr += green('\nKey: %s\nValue: %s\n' % (key, r.sunion(key)))
    logger.info(dumpStr)
    logger.info('==================== END OF REDIS DUMP ====================')


def flush_redis():
    logger.info("Deleting all Redis keys: '%s'" % ZKEY_AUTOCOMPLETE)
    r.flushdb()


# =====================================================================
# Main Functions for Autocomplete / Search Results
# =====================================================================
def search_redis(query, no_of_results=10, redis_stored_fields_only=True):
    """Finds search results based on a query"""
    logger.info("Query entered: %s and we want %s results." % (query, no_of_results))
    if query is None:
        return []
    if redis_stored_fields_only:
        return [_get_django_redis_model(result) for result in autocomplete_phrase(query, no_of_results)]
    else:
        return [_get_django_model(result) for result in autocomplete_phrase(query, no_of_results)]


def autocomplete_suggestion(phrase, no_of_results):
    if phrase is None:
        return []
    logger.debug("Autocompleting Suggestion: %s will try and find %s results" % (phrase, no_of_results))
    results = set()  # create (unique) set
    words = phrase.lower().split()
    logger.debug("Split Phrase: [ %s ] into [ %s ]" % (phrase, words))
    [results.update(_autocomplete_word(r, word, count=no_of_results)) for word in words]
    logger.info("results: %s" % results)
    return results


# ============================================================================
def autocomplete_phrase(phrase, no_of_results):
    """ Completes Phrase from stored Redis Phrases. """
    results = autocomplete_suggestion(phrase, 10000)
    keys = map(lambda k: SKEY_AUTOCOMPLETE+k, results)
    logger.debug("%s  autocomplete results: %s" % (keys, results))
    for key in keys:
        for member in r.smembers(key):
            logger.debug("key - %s  %s" % (key, r.smembers(key)))
            phrase = key.replace(SKEY_AUTOCOMPLETE, "")
            if r.zscore(ZKEY_AUTOCOMPLETE_SCORE, phrase+":"+member) is None:
                r.zincrby(ZKEY_TMP_SEARCH_RANKING, member, 1)
            else:
                r.zincrby(ZKEY_TMP_SEARCH_RANKING, member, r.zscore(ZKEY_AUTOCOMPLETE_SCORE, phrase+":"+member))
    logger.debug("zrangebyscore: %s" % r.zrangebyscore(ZKEY_TMP_SEARCH_RANKING, float("-inf"), float("inf")))
    res = r.zrangebyscore(ZKEY_TMP_SEARCH_RANKING, float("-inf"), float("+inf"))
    # Can now delete the tmp redis sorted set
    r.zremrangebyrank(ZKEY_TMP_SEARCH_RANKING, 0, -1)
    # Need to reverse as high scores has the highest index - not what we wank
    res.reverse()
    logger.debug("res: %s  %s" % (res, res[:no_of_results]))
    return res[:no_of_results]


def _get_django_redis_model(val):
    """ Retrieves stored cached django model from redis (only 'redis_stored_fields' fields) """
    logger.debug("_get_django_redis_model, %s - %s" % (val, r.sunion(SKEY_MODELS+val)))
    model, id = val.split(':')
    # app, model = content.split('.')
    # HACK - Create a json structure similar to a normal django model
    json_result = {
        "id": int(id),
        "model": "%s" % model,
    }
    for field in sorted(r.sunion(SKEY_MODELS+val), key=str.lower):
        field_name, field_val = field.split(":")
        json_result[field_name] = field_val
    return json_result


def _get_django_model(val):
    """ Get Django Model from string <model_meta>:<pk>
        The string must be of the format above.
        TODO: error checking
        THIS IS A SLOW METHOD BY COMPARISON  - PSQL AS OPPOSE TO REDIS
    """
    content, id = val.split(':')
    app, model = content.split('.')
    model = models.get_model(app, model)
    return model.objects.get(id=id)


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
        # Return a range of members in a sorted set by index
        entries = r.zrange(ZKEY_AUTOCOMPLETE, start, start + rangelen - 1)
        logger.info("entries:\n%s" % entries)
        if not entries or len(entries) == 0:
            break
        start += rangelen

        for entry in entries:
            minlen = min((len(entry), len(word)))
            if entry[:minlen] != word[:minlen]:
                return results   # Is this correct

            if entry[-1] == '*' and len(results) < count:
                results.add(entry[0:-1])
    logger.info("_autocomplete_word, results: %s" % results)
    return results
