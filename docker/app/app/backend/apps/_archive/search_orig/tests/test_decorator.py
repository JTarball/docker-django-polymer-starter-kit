from django import test

from django_dynamic_fixture import G

from project.test_factories.models import Article
from project.test_factories.model_factories import StaticFixtureClass
from search.decorators import Redis_Search


class TestRedisSearchDecorator(test.TestCase):
    """ Tests functionality of search decorator. """

    def setUp(self):
        G(Article, n=3)

    def test_model_with_no_category_and_no_url(self):
        Redis_Search("title", "body").__call__(Article)
