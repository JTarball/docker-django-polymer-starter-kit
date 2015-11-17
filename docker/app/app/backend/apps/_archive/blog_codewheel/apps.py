"""
apps.py - App Configuration for Blog App
"""
import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

logger = logging.getLogger('project_logger')


def my_callback(sender, **kwargs):
    function_name = 'my_callback'
    logger.info('Firing registered callback: %s from %s' % (function_name, sender))


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = "Blog"

    def ready(self):
        post_migrate.connect(my_callback, sender=self)