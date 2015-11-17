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

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.exceptions import ValidationError

# Redis search capability
import search
from search.decorator import Redis_Search











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
    parent = models.ForeignKey('self', related_name='other_subcategory', null=True, blank=True)
    child = models.ManyToManyField('self', null = True, blank = True ) 

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










class PostNode(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    #post = models.ManyToManyField(Post, null=True, blank=True)

    def __unicode__(self):
        return self.slug                        # return a string representation of our model


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
        self.content_markup = markdown2.markdown(self.content_markdown)
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):  # for routing urls (uses slug as title)
        return ('content:detail', (), {'slug': self.slug})


class Code(models.Model):
    """ Model for a code snippet. """
    title = models.CharField(('title'), max_length=100)
    slug    = models.SlugField(max_length=100, unique=True)
    post_date   = models.DateTimeField('Published Date',auto_now_add=True)
    updated_date = models.DateTimeField('Updated Date', auto_now=True)
    # Code
    content = models.TextField(('body'))
    content_comments = models.TextField(('body comments'))  # use to help search -- all comments in code as sentences
    uses = models.TextField()
    #language = models.ManyToManyField(Language)

    # Comments
    #comments = models.ForeignKey(Comment)


    @models.permalink
    def get_absolute_url(self): # for routing urls (uses slug as title)
        return ('catalog_category', (), { 'category_slug': self.slug })


class Comment(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comment = models.CharField(verbose_name=_(u'Comment'), max_length=255, help_text='Update Reason and describe changes')
    post = models.ForeignKey(Post)


class Update(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comment = models.CharField(verbose_name=_(u'Comment'), max_length=255, help_text='Update Reason and describe changes')
    post = models.ForeignKey(Post)


class Issue(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comment = models.CharField(verbose_name=_(u'Issues'), max_length=255, help_text='Update Reason and describe changes')
    post = models.ForeignKey(Post)







# Validation -- can add post if has children

