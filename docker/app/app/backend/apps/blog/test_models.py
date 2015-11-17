"""
    blog.test_models.py
    ==================

    Test Models for Blog App

"""
import datetime

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django_dynamic_fixture import G
from django_dynamic_fixture.ddf import BadDataError
from rest_framework.test import APITestCase

from accounts.models import AccountsUser
from blog.models import Post
from blog.utils import markup


class BlogTests(APITestCase):

    def setUp(self):
        self.staff = G(AccountsUser, is_superuser=False, is_staff=True)

    def test_model_creation(self):
        """ Basic test for Post model creation. """
        post = G(Post, title="This is a test post.", slug="", author=self.staff)
        self.assertTrue(post.content_markup, str(markup(post.content)))
        self.assertTrue(isinstance(post, Post))
        self.assertEquals(post.__unicode__(), post.title)
        self.assertEquals(post.slug, slugify(post.title))

    def test_model_url(self):
        """ Basic test for url creation. """
        post = G(Post, content="This is a test post.", author=self.staff)
        self.assertEquals(post.get_absolute_url(), reverse('blog:detail', kwargs={'slug': post.slug}))

    def test_custom_slug(self):
        """ Test for slug uniqueness and setting. """
        post = G(Post, content="This is a test post.", slug="slugged-post", author=self.staff)
        self.assertNotEqual(post.slug, slugify(post.title), "If slug field is set it shouldnt be equal to slugify().")
        self.assertEquals(post.slug, 'slugged-post', "If slug field is set it shouldn't be a slugify of the title.")

    def test_custom_slug_create_duplicate(self):
        """ A test to ensure slug doesnt create duplicates. """
        G(Post, title="A Post with a Custom Slug", slug="", author=self.staff)
        with self.assertRaises(BadDataError):  # CAN'T USE UTILS.INTEGRITYERROR BECAUSE OF DDF
            G(Post, title="A Post with a Custom Slug", slug="", author=self.staff)

    def test_live_posts(self):
        """ A test of live() method - should only return published posts. """
        live_post = G(Post, title="post 1", slug="", author=self.staff, published=True)
        draft_post = G(Post, title="post 2", slug="", author=self.staff, published=False)
        live_posts = Post.objects.live()
        self.assertTrue(live_post in live_posts)
        self.assertTrue(draft_post not in live_posts)

    def test_posts_by_user(self):
        """ A test to ensure all posts are returned for a specific author. """
        user1 = G(AccountsUser, is_superuser=False, is_staff=False)
        user2 = G(AccountsUser, is_superuser=False, is_staff=False)
        post1 = G(Post, author=user1, published=True)
        post2 = G(Post, author=user1, published=False)
        post3 = G(Post, author=user2, published=False)
        posts = Post.objects.by_user(user1)
        self.assertTrue(post1 in posts)
        self.assertTrue(post2 in posts)
        self.assertTrue(post3 not in posts)

    def test_posts_live_by_user(self):
        """ A test to ensure only publish posts are returned for a specific author. """
        user1 = G(AccountsUser, is_superuser=False, is_staff=False)
        user2 = G(AccountsUser, is_superuser=False, is_staff=False)
        post1 = G(Post, author=user1, published=True)
        post2 = G(Post, author=user1, published=False)
        post3 = G(Post, author=user2, published=False)
        posts = Post.objects.live_by_user(user1)
        self.assertTrue(post1 in posts)
        self.assertTrue(post2 not in posts)
        self.assertTrue(post3 not in posts)

    def test_posts_live_by_tag(self):
        """ A test to ensure only publish posts are returned for a specific tag. """
        user1 = G(AccountsUser, is_superuser=False, is_staff=False)
        user2 = G(AccountsUser, is_superuser=False, is_staff=False)
        post1 = G(Post, tags=['tag1'], author=user1, published=True)
        post2 = G(Post, tags=['tag2'], author=user1, published=True)
        post3 = G(Post, tags=['tag1'], author=user2, published=False)
        posts = Post.objects.live_by_tag('tag1')
        self.assertTrue(post1 in posts)
        self.assertTrue(post2 not in posts)
        self.assertTrue(post3 not in posts)

    def test_posts_by_year(self):
        """ A test to ensure all posts are returned for a specific year. """
        post_2011 = G(Post, updated_at=datetime.datetime(2011, 8, 22), published=True)
        post_2007 = G(Post, updated_at=datetime.datetime(2007, 7, 2), published=True)
        post_2008 = G(Post, updated_at=datetime.datetime(2008, 7, 2), published=True)
        post_2013 = G(Post, updated_at=datetime.datetime(2013, 1, 2), published=True)
        post_2013_not_published = G(Post, updated_at=datetime.datetime(2013, 1, 2), published=False)
        post_now = G(Post, published=True)
        posts_2013 = Post.objects.by_year('2013')
        self.assertTrue(post_now not in posts_2013)
        self.assertTrue(post_2013 in posts_2013)
        self.assertTrue(post_2013_not_published in posts_2013)
        self.assertTrue(post_2008 not in posts_2013)
        self.assertTrue(post_2007 not in posts_2013)
        self.assertTrue(post_2011 not in posts_2013)

    def test_posts_live_by_year(self):
        """ A test to ensure only published posts are returned for a specific year. """
        post_2011 = G(Post, updated_at=datetime.datetime(2011, 8, 22), published=True)
        post_2007 = G(Post, updated_at=datetime.datetime(2007, 7, 2), published=True)
        post_2008 = G(Post, updated_at=datetime.datetime(2008, 7, 2), published=True)
        post_2013 = G(Post, updated_at=datetime.datetime(2013, 1, 2), published=True)
        post_2013_not_published = G(Post, updated_at=datetime.datetime(2013, 1, 2), published=False)
        post_now = G(Post, published=True)
        posts_2013 = Post.objects.live_by_year('2013')
        self.assertTrue(post_now not in posts_2013)
        self.assertTrue(post_2013 in posts_2013)
        self.assertTrue(post_2013_not_published not in posts_2013)
        self.assertTrue(post_2008 not in posts_2013)
        self.assertTrue(post_2007 not in posts_2013)
        self.assertTrue(post_2011 not in posts_2013)
