import markdown2

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib import auth
from django.conf import settings

from apps.search.decorator import Redis_Search


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


# Simple Category Class should help navigate of blog entries
class Category(models.Model):
    title = models.CharField( verbose_name = _(u'Title'), help_text = _(u' '), max_length = 255 )
    slug = models.SlugField(max_length=255, editable=True)

    class Meta: 
        #app_label = _(u'blog') 
        verbose_name = _(u"Category") 
        verbose_name_plural = _(u"Categories") 
        ordering = ['title',] 
    
    def __unicode__(self):
        return self.title


# foreign key many update comments
class Update(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comment = models.CharField(verbose_name=_(u'Comment'), max_length=255, help_text='Update Reason and describe changes')


# Redis needs initial data
#@Redis_Search("title")
class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=True)
    content = models.TextField()
    content_markdown = models.TextField(verbose_name = _(u'Content (Markdown)'), help_text = _(u' '))
    content_markup = models.TextField(verbose_name = _(u'Content (Markup)'), help_text = _(u' '))
    published = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    # ===== Classification ===== #
    category = models.ManyToManyField(Category, verbose_name = _(u'Categories'), help_text = _(u' '), null = True, blank = True ) 
    changelog = models.ManyToManyField(Update, verbose_name=u'changelog', help_text=_(u' '), null=True, blank=True)
    # =====  SEO Stuff ===== #
    meta_keywords = models.CharField('Meta Keywords', max_length=255,
                                         help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')

    # add our custom model manager
    objects = PostManager()

    class Meta:
        #app_label = _(u'blog')
        ordering = ["-created_at", "title"]  # if two with same created_at use title.
        db_table = 'blog_post'
        verbose_name_plural = 'posts'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_markup = markdown2.markdown(self.content_markdown)
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):  # for routing urls (uses slug as title)
        return ('blog:detail', (), {'slug': self.slug})

