import logging
import re
from sets import Set
from difflib import unified_diff, context_diff, ndiff,get_close_matches


from markdown2 import markdown
# BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

from mptt.models import MPTTModel, TreeForeignKey

from django.db import models, backends
from django.conf import settings
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.db.models import signals
from django import forms

#from djangotoolbox.fields import ListField
from taggit.managers import TaggableManager
from taggit.models import Tag
from taggit.forms import TagField

# import our special markdown function
from blog.utils import cwmarkdown, find_all_commentable_tags
# Redis search capability
from search.utils import add_model_to_redis_search, flush_redis, log_dump_redis

# Get instance of logger
logger = logging.getLogger('project_logger')

##############################################################################
# Types
##############################################################################
COMMENT_TYPE_CHOICES = (
    (1, 'Comment'),
    (2, 'Issues'),
    (3, 'Troubleshooting'),
    (4, 'Updates'),
    (5, 'Code Examples'),
)


#from blog.forms.forms import StringListField
from django.utils.deconstruct import deconstructible


class StringListField(models.Field):
    u'''
    Save a list of strings in a CharField (or TextField) column.

    In the django model object the column is a list of strings.
    '''
    __metaclass__=models.SubfieldBase
    SPLIT_CHAR=u'\v'
    def __init__(self, *args, **kwargs):
        self.internal_type=kwargs.pop('internal_type', 'CharField') # or TextField
        super(StringListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return value.split(',')

    def get_internal_type(self):
        return self.internal_type

    def get_db_prep_lookup(self, lookup_type, value):
        # SQL WHERE
        raise NotImplementedError()

    def get_db_prep_save(self, value, connection=None):
        print value, "value", type(value)
        if value is None: return None
        return ', '.join(value)

    def formfield(self, **kwargs):
        assert not kwargs, kwargs
        return forms.CharField()



class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        print "to_python, ListField"
        print type(value), value
        if not value:
            value = []

        if isinstance(value, list):
            print "is list"
            return value

        return [item.strip() for item in value.split(',')]

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
    #def formfield(self, **kwargs):
    #    return models.Field.formfield(self, StringListField, **kwargs)

class CategoryField(ListField):
    def db_type(self, connection):
        return 'listtype'

    def to_python(self, value):
        logger.info('to_python')
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)

class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        logger.info('to_python')
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        logger.error("%s" % value)
        #for val in value.strip().split(','):
        #    print val, "val"
        return self.token.join([s for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def formfield(self, **kwargs):
        return models.Field.formfield(self, TagField, **kwargs)





##############################################################################
# Managers
##############################################################################
class PostRevisionManager(models.Manager):
    def create_post_revision(self, post, content, comment):
        version = self.create(content=content, comment=comment)
        post.versions.add(version)


class PostManager(models.Manager):
    use_for_related_fields = True

    def live(self): 
        """ Returns all published blog articles. """
        return self.model.objects.filter(published=True)

    def live_by_user(self, user):
        """ 
        Returns published blog posts for a specified user.
        user - string of username
        """
        try:
            user_id = auth.get_user_model().objects.get(username=user).id
        except:
            user_id = None
        return self.model.objects.filter(published=True, author_id=user_id)

    def live_by_year(self, year):
        return self.model.objects.filter(created_at__year=year)

    def live_by_category(self, category):
        return self.model.objects.filter(category__slug=category)


class CommentManager(models.Manager):
    def get_ids(self):
        logger.info('post_idnames, %s' % [comment.idname for comment in self.model.objects.all()])
        return [comment.idname for comment in self.model.objects.all()]
##############################################################################
# Folder
##############################################################################

class PostNode(MPTTModel):
    # For Redis Search only #############
    searchable_fields = ['name']
    redis_stored_fields = ['name', 'get_absolute_url'] # These are fields for the model which are saved to Redis. for fast access (stop gap for noSQL database)
    #####################################
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, editable=True)
    description = models.TextField(help_text = _(u' '), blank=True)
    language = TreeForeignKey('self', null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    #post = models.ManyToManyField(Post, null=True, blank=True)
    def save(self, *args, **kwargs):
        try:
            self.language =  self.get_root()
        except: pass
        return super(PostNode, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.level) + self.slug                        # return a string representation of our model

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        if self.parent:
            return reverse('blog:listsmall', kwargs={'language': self.language.slug, 'parent': self.slug})
        else:
            return reverse('blog:language', kwargs={'language': self.slug})


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    type = models.PositiveSmallIntegerField(choices=COMMENT_TYPE_CHOICES, default=1)
    content = models.TextField(default="this is the default comment.")
    #synced =  models.BooleanField(default=False)
    idname = models.CharField(max_length=8) # id to link to paragraph
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    # Is this a comment a reply to a post? ( Only relevant for comments, warnings )
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', related_name='commentreply', blank=True, null=True)
    objects = CommentManager()

##############################################################################
# Post
##############################################################################
# Ok - had problems in admin with comma separated string Models and because only allow one Tag Model Manager
# so...
# 
class VirtualTag(models.Model):
    name = models.CharField(verbose_name=_('Name'), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("vtag")
        verbose_name_plural = _("vtags")


##############################################################################
# Post Revision
##############################################################################
class PostRevision(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_revisions")
    created_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "created_%(app_label)s_%(class)s_set")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "modified_%(app_label)s_%(class)s_set")
    content = models.TextField()
    comment = models.CharField(verbose_name=_(u'Comment'), max_length=255)
    objects = PostRevisionManager() 


# /home/language/category/subcategory/slug
# auyjor>>>>>author gor comments
# editor should tell user not the same as published ocntent
class Post(models.Model):
    # For Redis Search only #############
    searchable_fields = ['title', 'tags']
    searchable_fields_options = {'title': {'OnlyPhrase': True}}
    redis_stored_fields = ['title', 'slug', 'get_absolute_url'] # These are fields for the model which are saved to Redis. for fast access (stop gap for noSQL database)
    #####################################
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    # created_by? - use postrevision instead?
    # updated_by? - use postrevision instead? remember update major


    published = models.BooleanField(default=True)
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    # Markdown content
    content = models.TextField(default="this is the default content.")
    # Markup from markdown
    content_markup = models.TextField(blank=True, verbose_name = _(u'Content (Markdown)'), help_text = _(u' '))
    # Commit revision
    update_comment =  models.CharField(verbose_name=_(u'Commit Comment'), max_length=255)#models.ForeignKey(Revision)
    # This is a major update and will be recorded 
    update_major = models.BooleanField(default=True) 
    node = models.ForeignKey(PostNode, null=True, blank=True)
    
    
    include_tags = models.ManyToManyField(VirtualTag, blank=True, related_name="include_tags")
    exclude_tags = models.ManyToManyField(VirtualTag, blank=True, related_name="exclude_tags")
    #excluding_tags = CategoryField(blank=True, null=True)
    #including_tags = SeparatedValuesField(null=True, blank=True, help_text='These are tags which will be always included on every save. Perfect for manual tags.')
    tags = TaggableManager(blank=True)
    comments = models.ManyToManyField(Comment, blank=True, help_text="If you save here - the normal save will be overridden by save_related in the adminModel")
    versions = models.ManyToManyField(PostRevision, blank=True)
    # add our custom model manager
    objects = PostManager()
    

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy('blog:detail', kwargs={'language': u'python', 'parent': u'theory', 'slug': u'hello-world'})


    # VERY IMPORTANT IF ROOT NODE THAT THE SLUG BE UNIQUE
    def save(self, *args, **kwargs):
        # If this is a major commit update the html content in the post.
        if self.update_major:
            # If first revision, markup content
            # Else it is a bit more tricky. In order to synchronise comments
            # to commentable html tags we have to go through a few hoops.
            if not self.content_markup:
                self.content_markup = str(cwmarkdown(self.content))
            else:
                self.content_markup = str(cwmarkdown(self.content, previous_content=self.content_markup, post=self, comments=self.comments))

            if self.content and self.pk:
                # Note: Any change here needs to be reflected in save_related in admin.py
                # Add Root Node & Section Node & any manual tags by Default - Language, Subsection in this case
                default_tags = []
                if self.include_tags:
                    default_tags = [tag.name for tag in self.include_tags.all()]
                default_tags.extend([self.node.name.lower(), self.node.parent.name.lower()])
                contTags = Set(default_tags)

                # Find any tags from content and auto-add
                for tag in Tag.objects.all():
                    if re.search( tag.name, self.content, re.M|re.I):
                        contTags.add(tag)

                # Remove any tags which are from exclude tags
                if self.exclude_tags:
                    exclude_tags = [exclude_tag.name for exclude_tag in self.exclude_tags.all()]
                    contTags = Set([tag for tag in contTags if tag not in exclude_tags])

                # Finally clear tags completely and readd
                self.tags.clear()
                for tag in contTags:
                    self.tags.add(tag)

        if not self.slug:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
        
        # Finally, save a revision - commit
        print self.id
        PostRevision.objects.create_post_revision(post=self, content=self.content, comment=self.update_comment)


##############################################################################
# Comment - type of comment (warning/ issue / comment)
##############################################################################
def reindex_redis_search(sender, instance, **kwargs):
    """ Callback function which recalculates what is searchable in redis from sender. """
    logger.info("Re-creating Search Autocomplete Index ...")
    flush_redis()
    [add_model_to_redis_search(model) for model in Post.objects.all()]
    [add_model_to_redis_search(model) for model in PostNode.objects.all()]
    log_dump_redis()

signals.post_save.connect(reindex_redis_search, sender=Post, dispatch_uid="add_post_tags")


