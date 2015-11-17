"""
    blog.models
    ===========

    Models file for a basic Blog App

"""
import logging
import datetime
from dateutil import relativedelta

from taggit.managers import TaggableManager

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from blog.utils import markup, toTimeAgo
from search.utils import add_model_to_redis, dump_redis, flush_redis
# Get instance of logger
logger = logging.getLogger('project_logger')


class PostManager(models.Manager):
    use_for_related_fields = True

    def live(self):
        """ Returns all published blog articles. """
        return self.model.objects.filter(published=True)

    def by_year(self, year):
        return self.model.objects.filter(updated_at__year=year)

    def live_by_year(self, year):
        return self.model.objects.filter(updated_at__year=year, published=True)

    def by_tag(self, tag):
        return self.model.objects.filter(tags__name__in=[tag]).distinct()

    def live_by_tag(self, tag):
        return self.model.objects.filter(tags__name__in=[tag], published=True).distinct()

    def by_user(self, user):
        try:
            user_id = get_user_model().objects.get(username=user).id
        except:
            user_id = None
        return self.model.objects.filter(author_id=user_id)

    def live_by_user(self, user):
        try:
            user_id = get_user_model().objects.get(username=user).id
        except:
            user_id = None
        return self.model.objects.filter(author_id=user_id, published=True)


class Post(models.Model):
    """ Blog Post Model. """
    # =====================
    # For Redis Search Only
    # =====================
    searchable_fields = ['title', 'tags']
    # These are fields for the model which are saved to Redis. for fast access (stop gap for noSQL database)
    redis_stored_fields = ['title', 'slug', 'get_absolute_url']
    # ======================
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    content_markup = models.TextField(blank=True, verbose_name=_(u'Content (Markdown)'), help_text=_(u' '))
    published = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Beautified fields
    # date_ago = models.CharField(blank=True, max_length=255) # not currently used
    updated_at_beautified = models.CharField(blank=True, max_length=50)
    author_name = models.CharField(blank=True, max_length=50)
    tags = TaggableManager(blank=True)
    # add our custom model manager
    objects = PostManager()

    def __unicode__(self):
        return self.title

    def timeAgo(self):
        return toTimeAgo(relativedelta.relativedelta(datetime.datetime.now(), self.updated_at))

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})

    def save(self, *args, **kwargs):
        self.content_markup = str(markup(self.content))
        self.author_name = str(get_user_model().objects.get(id=self.author.id).username)
        if isinstance(self.updated_at, datetime.date):
            self.updated_at_beautified = str(self.updated_at.today().strftime('%d, %b %Y'))
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


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
