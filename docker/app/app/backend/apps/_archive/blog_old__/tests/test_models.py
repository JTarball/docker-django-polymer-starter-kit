"""
Blog app tests for models

Requirements to run correctly: requires sqlite3 as database
"""
import datetime

from django.db import utils
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings

from django_dynamic_fixture import G

from project.test_factories.model_factories import UserStaticFixtureClass
from ..models import Post


class BlogTests(TestCase):

    def setUp(self):
        user_str = settings.AUTH_USER_MODEL
        app_name, model_name = user_str.split('.')
        self.user = G(get_model(app_name, model_name), is_superuser=True, is_staff=True, data_fixture=UserStaticFixtureClass())
        self.different_user = G(get_model(app_name, model_name),username='dsg106', is_superuser=True, is_staff=True, data_fixture=UserStaticFixtureClass())

    def create_post(self, title='Test Blog Post', user=None, published=True):
        if user is None: user = self.user
        return Post.objects.create(
            title = title,
            author = user,
            published = published
            )

    # ====== Basic 'does it work' Tests ========================= #
    def test_model_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__unicode__(), post.title)
        self.assertEqual(post.slug, slugify(post.title))

    def test_model_url(self):
        post = self.create_post()
        self.assertEqual(post.get_absolute_url(), reverse('blog:detail', kwargs={'slug': post.slug}))

    def test_model_manager(self):
        live_post = self.create_post(title='post 1')
        draft_post = self.create_post(title='post 2', published=False)
        self.assertIn(live_post, Post.objects.live())
        self.assertNotIn(draft_post, Post.objects.live())

    # ====== Specific Simple Tests ============== #
    def test_custom_slug(self):
        post = Post.objects.create(
            title='A Post with a Custom Slug',
            slug='woah',
            author=self.user
            )
        self.assertNotEqual(post.slug, slugify(post.title))
        self.assertEqual(post.slug, 'woah')

    def test_custom_slug_create_duplicate(self):
        """ A test to ensure slug doesnt create duplicates. """
        Post.objects.create(
            title='A Post with a Custom  Slug',
            slug='woah',
            author=self.user
            )
        with self.assertRaises(utils.IntegrityError):
            self.create_post(title='woah')
        with self.assertRaises(utils.IntegrityError):
            Post.objects.create(
                title='Another Post with a Custom  Slug',
                slug='woah',
                author=self.user
                )

    def test_live_posts(self):
        live_post = self.create_post(title='post 1')
        draft_post = self.create_post(title='post 2', published=False)
        live_posts = Post.objects.live()
        self.assertTrue(live_post in live_posts)
        self.assertTrue(draft_post not in live_posts)

    def test_live_by_user(self):
        live_post_userA = self.create_post(title='blog post 1')
        draft_post_userA = self.create_post(title='blog post 2', published=False)
        live_post_userB = self.create_post(title='blog post 3', user=self.different_user)
        draft_post_userB = self.create_post(title='blog post 4', user=self.different_user, published=False)
        self.assertIn(live_post_userA, Post.objects.live_by_user(self.user.username), msg='live_by_user should only contain posts from a specific user. Posts found doesnt include generated live post from author.')
        self.assertNotIn(draft_post_userA, Post.objects.live_by_user(self.user.username), msg='live_by_user should only contain posts which have been published. Not draft posts.')
        self.assertNotIn(live_post_userB, Post.objects.live_by_user(self.user.username), msg='live_by_user should only contain posts from a specific user. Posts found include ones from a different user.')
        self.assertNotIn(draft_post_userB, Post.objects.live_by_user(self.user.username), msg='live_by_user should only contain posts which have been published. Not draft from different users.')

    def test_posts_by_user_no_user_found(self):
        """ Tests that all published posts are returned if no user is found. """
        self.create_post()
        self.create_post(title='A random post')
        self.create_post(title='Another random post', published=False)
        for post in Post.objects.live():
            self.assertIn(post, Post.objects.live_by_user('woahuser'), msg='a published post has not been found in posts generated where no user is found.')

    def test_posts_by_year(self):
        post_2011 = G(Post, created_at=datetime.datetime(2009, 8, 22))
        post_2007 = G(Post, created_at=datetime.datetime(2007, 7, 2))
        post_2008 = G(Post, created_at=datetime.datetime(2008, 7, 2))
        post_2013 = G(Post, created_at=datetime.datetime(2013, 1, 2))
        post_now = self.create_post()
        posts_2013 = Post.objects.live_by_year('2013')
        self.assertTrue(post_now in posts_2013)
        self.assertTrue(post_2013 in posts_2013)
        self.assertTrue(post_2008 not in posts_2013)
        self.assertTrue(post_2007 not in posts_2013)
        self.assertTrue(post_2011 not in posts_2013)

