#!/usr/bin/env python
"""
    tests.models
    ============

    Models for testing only

"""
from taggit.managers import TaggableManager

from django.db.models import signals
from django.db import models
from django.template.defaultfilters import slugify

from search.utils import add_model_to_redis, dump_redis, flush_redis


class TestModelPost(models.Model):
    """ Test Model - Post like Model """
    # =====================
    # For Redis Search Only
    # =====================
    searchable_fields = ['title', 'tags']
    redis_stored_fields = ['title', 'slug', 'get_absolute_url']
    # ======================
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(TestModelPost, self).save(*args, **kwargs)


##############################################################################
# Comment - type of comment (warning/ issue / comment)
##############################################################################
def reindex_redis_search(sender, instance, **kwargs):
    """ Callback function which recalculates what is searchable in redis from sender. """
    flush_redis()
    [add_model_to_redis(model) for model in TestModelPost.objects.all()]
    dump_redis()

signals.post_save.connect(reindex_redis_search, sender=TestModelPost, dispatch_uid="add_post_tags")
