"""
    Generic Simple Django Model for Testing.
    Idea is to keep all models here if possible.
    Remember DRY (Do Not Repeat Yourself!)
"""
from django.db import models
from django.template.defaultfilters import slugify

from project.settings import base as settings


class Article(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
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


class ArticleNoUrl(Article):

    def __init__(self):
        self.delattr('url')
        super(Article, self).__init__()


class ArticleNoCategory(Article):

    def __init__(self):
        self.delattr('category')
        super(Article, self).__init__()


class ArticleNoUrlNoCategory(Article):

    def __init__(self):
        self.delattr('url')
        self.delattr('category')
        super(Article, self).__init__()
