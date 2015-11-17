"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings

from django_dynamic_fixture import G

from project.test_factories.model_factories import UserStaticFixtureClass
from ..models import Post


class BlogViewTests(TestCase):
    def setUp(self):
        user_str = settings.AUTH_USER_MODEL
        app_name, model_name = user_str.split('.')
        self.user = G(get_model(app_name, model_name), is_superuser=True, is_staff=True, data_fixture=UserStaticFixtureClass())
        self.live_post = G(Post, title='This is a live post', slug='woah', author=self.user)
        self.live_post_2011 = G(Post, title='This is a live post from 2011', created_at=datetime.datetime(2011,2,2), author=self.user)
        self.draft_post = G(Post, title='This is not a live post', slug='notsowoah', author=self.user, published=False)

    def test_list_view(self):
        url = reverse('blog:list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')
        self.assertIn(self.live_post.title, resp.rendered_content)

    def test_list_by_user_view(self):
        url = reverse('blog:list_user', kwargs={'username':self.live_post.author.username})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')
        self.assertIn(self.live_post.title, resp.rendered_content)

    def test_list_by_year_view(self):
        url = reverse('blog:list_year', kwargs={'year':'2011'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')
        self.assertIn(self.live_post_2011.title, resp.rendered_content)
        self.assertNotIn(self.live_post.title, resp.rendered_content)

   # def test_list_by_cat_view(self):
    #     url = reverse('blog:list')
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTemplateUsed(resp, 'blog/post_list.html')
    #     self.assertIn(self.live_post.title, resp.rendered_content)

    def test_detail_view(self):
        url = reverse('blog:detail', kwargs={'slug':self.live_post.slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_detail.html')
        self.assertIn(self.live_post.title, resp.rendered_content)



