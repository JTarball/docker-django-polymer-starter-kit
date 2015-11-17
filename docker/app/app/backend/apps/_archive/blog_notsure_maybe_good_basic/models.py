"""
    blog.models
    ===========
 
    Models file for a basic Blog App

"""
import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from blog.utils import markup


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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    abstract = models.TextField()
    content = models.TextField()
    content_markup = models.TextField(blank=True, verbose_name = _(u'Content (Markdown)'), help_text = _(u' '))
    published = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # add our custom model manager
    objects = PostManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})

    def save(self, *args, **kwargs):
        self.content_markup = markup(self.content)
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

