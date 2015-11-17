<a href="http://www.djangoproject.com/" >
	<img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" />
</a>

## 'search' App

A 'search' app powered by Redis

- simple & basic
- add high speed autocomplete and search querys using Redis



PLEASE EXPLAIN PROS / CONS OFCURRENT SEARCH ALGORITHM


How to use
==========
        How to add search to django model:
        ----------------------------------
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


        How to get autocomplete results:
        --------------------------------
        - the django view that is called is: views.AutoCompleteSuggestionsView.as_view() 
        - you get json 'django model like' result from an ajax call to: <url "autosuggestions">/q?="<word_to_autcomplete>"n?=<number_of_autosuggestions>
        
        How to get search results:
        --------------------------
        - the django view that is called is: views.SearchQueryPjaxView.as_view()
        - you get json 'django model like' result from an ajax call to: <url "results">/q?="search_word_or_phrase"n?=<no_of_results>               
