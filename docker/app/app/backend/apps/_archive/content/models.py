"""
# ============================================================================ #
# models.py
# 
# Author : Danvir Guram
# Date   : 16/6/2012
#
# Models for Content App
#
# Description:     Post Model - a page of something
#                  Code Model - a snippet of code
#                  Bug        - A description of a Bug
#                  Question   - A Question 
#    url description    root - Language - LanguageConstruct - Page
# ============================================================================ #
"""
import markdown2
import datetime

from dateutil import relativedelta

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.exceptions import ValidationError

# Redis search capability
import search
from search.decorator import Redis_Search





# MOVE THIS HELPER FUNCTION
# Helper function
def toTimeAgo(reldate):
    """ creates string from relativedelta. 
        NOTE: no type checking and expects relativedelta to be positive (could be negative).
        FIXME: fix above
    """
    reldate_str = "ago."
    if reldate.years > 0:
        reldate_str = str(reldate.years) + " years "+ reldate_str
    else:
        if reldate.months > 0:
            reldate_str = str(reldate.months) + " months "+ reldate_str
        else:
            if reldate.days > 0:
                reldate_str = str(reldate.days) + " days "+ reldate_str
            else:
                if reldate.hours > 0:
                    reldate_str = str(reldate.hours) + " hrs "+ reldate_str
                else:
                    reldate_str = str(reldate.minutes) + " mins "+ reldate_str
    return reldate_str

    
def beautifyData(number):
    """ Turns number into beautiful string.
        e.g.
        1,000,000,000 ---> 1G
        1,000,000     ---> 100M
        10,000        ---> 10K
        10            ---> 10
    """
    if not isinstance(number, (int, long, float)): return "NAN"
    if number > 1000000000:
        return str(number/1000000000) + "G"
    elif number > 1000000:
        return str(number/1000000) + "M"
    elif number > 1000:
        return str(number/1000) + "K"
    else:
        return str(number)


from mptt.models import MPTTModel, TreeForeignKey

class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name                        # return a string representation of our model




















# ========================================================================== #
# Main Model Manager for Post
# ========================================================================== #
class PostManager(models.Manager):
    use_for_related_fields = True

    def live(self): 
        """ Returns all published blog articles. """
        return self.model.objects.filter(published=True)

# NEED TO ADD COMMENT ABOUT CONNECT SO ... LANGUAGE, CATEGORY AND SUB
    def live_by_subcategory(self, language): 
        """ Returns all published blog articles. """
        return self.model.objects.filter(published=True, language__slug=language)


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

    def live_by_language(self, language):
        return self.model.objects.filter(language__slug=language)


# ============================================================================ #
# Helper Functions  -   REVIEW: move to an utils app                           #
# ============================================================================ #
#from unidecode import unidecode
#from django.template import defaultfilters
#def slugify(text):
#    """ Slugify single text """
#    slug = defaultfilters.slugify(unidecode(input_text))



# ============================================================================ #
# URL and general layout of web content
# foreign key many update comments


































# ========================== #
# Language                   #
# ========================== #
class Language(models.Model):
    """ A category model for languages in the most general sense. """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Used for URL. ')
    description = models.CharField(verbose_name=_(u'description'), max_length=255, help_text='Description of the Language.', blank=True)    

    # DB Stuff #
    class Meta:
        #db_table = 'content_category_languages'          # name in the database
        ordering = ['-slug']                              # ordering when retrieved more than one object from the database.
        verbose_name_plural = 'languages' 

    def __unicode__(self):
        return self.name                                  # return a string representation of our model

    @models.permalink
    def get_absolute_url(self): # for routing urls (uses slug as title)
        return ('content:language', (), { 'language': self.slug })    


# # ========================== #
# # Category                   #
# # ========================== #
# # Language/Language Constructs should be added to through the admin
class Category(models.Model):
    """ A category model for languages in the most general sense. """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Used for URL. ')
    language = models.ManyToManyField(Language, null = True, blank = True )
    


    # Database Stuff
    class Meta:
        #db_table = 'content_category_languages'          # name in the database
        ordering = ['-slug']                    # ordering when retrieved more than one object from the database.
        verbose_name_plural = 'categories' 

    def __unicode__(self):
        return self.name                        # return a string representation of our model

    @models.permalink
    def get_absolute_url(self): # for routing urls (uses slug as title)
        return ('content:category', (), { 'category': self.slug })


# ========================== #
# Sub-Category               #
# ========================== #
# Language/Language Constructs should be added to through the admin
# Note: Inheritance from Language

class SubCategory(models.Model):
    """ model class containing information about a category in the product catalog """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Used for URL. ') 
    category = models.ManyToManyField(Category, null = True, blank = True )

    def __unicode__(self):
        return self.name                        # return a string representation of our model

    # Database Stuff
    class Meta:
        #db_table = 'content_sub-category_language_constructs'   # name in the database
        ordering = ['-slug'] # ordering when retrieved more than one object from the database.
        verbose_name_plural = 'SubCategories' 

    @models.permalink
    def get_absolute_url(self): # for routing urls (uses slug as title)
        return ('content:subcategory', (), { 'subcategory': self.slug })

    def save(self, *args, **kwargs):
        print self.child.all()
        if self.child.all() is None: super(SubCategory, self).save(*args, **kwargs)
        children = [child.id for child in self.child.all()]
        print children
        if self.parent is not None:
            if self.parent.id in children:
                print "EROORRORO!"
                ValidationError('You have not met a constraint!')
            else:
                super(SubCategory, self).save(*args, **kwargs)
        else:
            super(SubCategory, self).save(*args, **kwargs)







#/language/category/subcategory/...../post_slug

# # Create Dynamic URL tree
# class Node(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(max_length=50, unique=True, help_text='Used for URL. ')  
#     # where does the dynamic tree start from   
#     language = models.ForeignKey(Language, related_name='root', null=True, blank=True)
#     category = models.ForeignKey(Category, related_name='root', null=True, blank=True)
#     subcategory = models.ForeignKey(SubCategory, related_name='root', null=True, blank=True)

#     parent = models.ForeignKey('self', related_name='other_subcategory', null=True, blank=True)
#     child = models.ManyToManyField('self', null = True, blank = True )
    
#     def __unicode__(self):
#         return self.name                        # return a string representation of our model

#     def save(self, *args, **kwargs):
#         if self.child.all() is None: super(Node, self).save(*args, **kwargs)
#         children = [child.id for child in self.child.all()]
#         print children
#         if self.parent is not None:
#             if self.parent.id in children:
#                 ValidationError('You have not met a constraint!')
#             else:
#                 super(Node, self).save(*args, **kwargs)
#         else:
#             super(Node, self).save(*args, **kwargs)




class Node():
     name = models.CharField(max_length=50)
     slug = models.SlugField(max_length=50, unique=True, help_text='Used for URL. ')     















class PostNode(MPTTModel):
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, editable=True)
    description = models.TextField(help_text = _(u' '), blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    #post = models.ManyToManyField(Post, null=True, blank=True)

    def __unicode__(self):
        return str(self.level) + self.slug                        # return a string representation of our model

    @models.permalink
    def get_absolute_url(self):  # for routing urls (uses slug as title)
        return ('', (), {'slug': self.slug})



        
# if no child then post


# =================================== #
# Post   # must define url  FIXME: needs to be in database first
# =================================== #
#@Redis_Search("title") 
class Post(models.Model):
    """ Model for posting a Page. """
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=True)

    content = models.TextField()
    content_markdown = models.TextField(verbose_name = _(u'Content (Markdown)'), help_text = _(u' '))
    content_markup = models.TextField(verbose_name = _(u'Content (Markup)'), help_text = _(u' '))

    content_codeexamples = models.TextField(null=True, blank=True, default='code examples')
    content_designdecisions = models.TextField(null=True, blank=True, default='design decisions')
    content_furtherlearning = models.TextField(null=True, blank=True, default='further learning')
    content_demo = models.TextField(null=True, blank=True, default='demo')
    content_gotchas = models.TextField(null=True, blank=True, default='gotcha')
    content_trickstips = models.TextField(null=True, blank=True, default='trickstips')

    published = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # ===== Classification ===== #
    #language = models.ManyToManyField(Language, related_name='language')
    #category = models.ManyToManyField(Category, related_name='category', verbose_name = _(u'Categories'), help_text = _(u' '), null = True, blank = True )
    node = models.ForeignKey(PostNode, null=True, blank=True)
    #subcategory = models.ManyToManyField(SubCategory, related_name='subcategory')
     # ===== Extra Stuff ===== #
    #update = models.ManyToManyField(Update, verbose_name=u'changelog', help_text=_(u' '), null=True, blank=True)
    #issue = models.ManyToManyField(Issue, verbose_name=u'issue', help_text=_(u' '), null=True, blank=True)
    # =====  SEO Stuff ===== #
    meta_keywords = models.CharField('Meta Keywords', max_length=255,
                                         help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
     # add our custom model manager
    objects = PostManager()

    def __unicode__(self):
        return self.title # return a string representation of our model

    def save(self, *args, **kwargs):
        print "SAVE!!!!!!!!!!!!!"
        self.content_markup = markdown2.markdown(self.content)
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):  # for routing urls (uses slug as title)
        return ('content:detail', (), {'slug': self.slug})

import os

def get_image_path(instance, filename):
    return os.path.join('post_screenshots', filename)


class PostCard(models.Model):
    """ A simple Post Model to be displayed as a card.
        Specifically this is different from other Posts from the fact that it
        could be a link to a different website
    """
    main_post = models.ForeignKey(Post)
    title =  models.CharField(verbose_name=_(u'Title'), max_length=255, help_text=_(u"What's the title?"))
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    content = models.TextField(blank=True, help_text=_(u"Add Content - if a Code Example: Put Code Here!"))
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=False, editable=True)
    likes = models.BigIntegerField(default=0, blank=True, null=True)
    views = models.BigIntegerField(default=0, blank=True, null=True)
    # Beautify 
    likes_pretty = models.CharField(max_length=10, default=0)
    views_pretty = models.CharField(max_length=10, default=0)
    comments_pretty = models.CharField(max_length=10, default=0)
    created_at_pretty = models.CharField(max_length=50, default=0)
    # APP USE NOTE: is_externalweb needs to true to use externalwebhref`
    is_externalhref = models.BooleanField(default=False, help_text=_(u"Is this a link to an external website?"))
    href = models.CharField(null=True, max_length=255, blank=True, help_text=_(u"What is the link to the external website"))

    # Broken HREF count #  for now to allow admin to see what needs checking first
    # can compare counts between cards
    brokens = models.BigIntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        self.likes_pretty = beautifyData(self.likes)
        self.views_pretty = beautifyData(self.views)
        self.comments_pretty = beautifyData(len(CommentCard.objects.filter(post=self)))
        #self.updated_at = datetime.datetime.now()
        self.created_at_pretty = toTimeAgo(relativedelta.relativedelta(datetime.datetime.now(), self.created_at))
        if not self.slug:
            self.slug = slugify(self.title)
        super(PostCard, self).save(*args, **kwargs)


    #@models.permalink
    #def get_absolute_url(self):  # for routing urls (uses slug as title)
    #     return ('content:detail', (), {'slug': self.main_post.slug})


class Liker(models.Model):
    """ A model to describe a Liker - useful for collect who has liked what. """
    card = models.ForeignKey(PostCard)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    liked_at = models.DateTimeField(auto_now_add=True, editable=True)





# Note: In future might be better to change Update, Issue, Troubleshooting, Dependency 
# into a field in Comment e.g. type 
# That way we only have one class Comment - which is cleaner
# 
# 

# Abstract Class #############################################################
class AbstractCommentModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    author_pretty = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(editable=False)
    date_ago = models.CharField(blank=True, max_length=255)
    comment = models.CharField(verbose_name=_(u'Comment'), max_length=255, help_text='Update Reason and describe changes')
    length = models.PositiveIntegerField(blank=True)
    reported = models.BooleanField(default=False)
    
    # Is this a comment a reply to a post
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', related_name='postreply', blank=True, null=True)


    def forceDateAgo(self):
        self.date_ago = toTimeAgo(relativedelta.relativedelta(datetime.datetime.now(), self.created_at))
        self.save()

    def __getattr__(self, name):
        self.date_ago = toTimeAgo(relativedelta.relativedelta(datetime.datetime.now(), self.created_at))
        self.save()
        return super(AbstractCommentModel, self).__getattr__(self, name);

    def save(self, *args, **kwargs):
        # created_at must be before other date
        self.author_pretty = self.author.username
        self.updated_at = datetime.datetime.now()
        self.date_ago = toTimeAgo(relativedelta.relativedelta(datetime.datetime.now(), self.updated_at))
        self.length = len(self.comment)
        super(AbstractCommentModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

##############################################################################
class Comment(AbstractCommentModel):
    post = models.ForeignKey(Post, null=True)


class CommentCard(AbstractCommentModel):
    # DSG NOTE: use postcard here
    post = models.ForeignKey(PostCard, null=True)


class Update(AbstractCommentModel):
    post = models.ForeignKey(Post, null=True)


class Issue(AbstractCommentModel):
    post = models.ForeignKey(Post)


class Troubleshooting(AbstractCommentModel):
    post = models.ForeignKey(Post)


class Dependency(AbstractCommentModel):
    post = models.ForeignKey(Post)

