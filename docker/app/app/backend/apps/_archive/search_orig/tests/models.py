"""
Simple Models used for Testing Only.
"""
from django.db import models
from django.template.defaultfilters import slugify

from search.decorator import Redis_Search


@Redis_Search("title", "body")
class Post(models.Model):
    """ Basic Post Model with no URL / Category fields. """
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=255)
    slug = models.SlugField(max_length=255, editable=True)
    url = models.TextField(max_length=20)
    category = models.TextField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class PostAbsoluteUrl(Post):
    """ Post Model with get_absolute_url function. """
    @models.permalink
    def get_absolute_url(self):  # for routing urls (uses slug as title)
        return ('catalog_category', (), {'category_slug': self.slug})
