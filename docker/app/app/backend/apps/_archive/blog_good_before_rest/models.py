"""
    blog.models
    ===========

    Models file for a basic Blog App

"""
import logging

from taggit.managers import TaggableManager

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from rest_framework import serializers

from blog.utils import markup
from search.utils import add_model_to_redis, dump_redis, flush_redis
# Get instance of logger
logger = logging.getLogger('project_logger')


class PostManager(models.Manager):
    use_for_related_fields = True

    def live(self):
        """ Returns all published blog articles. """
        return self.model.objects.filter(published=True)

    def live_by_year(self, year):
        return self.model.objects.filter(created_at__year=year)


class Post(models.Model):
    """ Blog Post Model. """
    # =====================
    # For Redis Search Only
    # =====================
    searchable_fields = ['title']
    # searchable_fields_options = {'title': {'OnlyPhrase': True}}
    # redis_stored_fields = ['title', 'slug', 'get_absolute_url'] # These are fields for the model which are saved to Redis. for fast access (stop gap for noSQL database)
    redis_stored_fields = ['title', 'slug', 'get_absolute_url']
    # ======================
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField()
    content_markup = models.TextField(blank=True, verbose_name=_(u'Content (Markdown)'), help_text=_(u' '))
    published = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = TaggableManager(blank=True)
    # add our custom model manager
    objects = PostManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})

    def save(self, *args, **kwargs):
        self.content_markup = str(markup(self.content))
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'content')


##############################################################################
# Comment - type of comment (warning/ issue / comment)
##############################################################################
def reindex_redis_search(sender, instance, **kwargs):
    """ Callback function which recalculates what is searchable in redis from sender. """
    logger.info("Re-creating Search Autocomplete Index ...")
    flush_redis()
    [add_model_to_redis(model) for model in Post.objects.all()]
    dump_redis()

signals.post_save.connect(reindex_redis_search, sender=Post, dispatch_uid="add_post_tags")
