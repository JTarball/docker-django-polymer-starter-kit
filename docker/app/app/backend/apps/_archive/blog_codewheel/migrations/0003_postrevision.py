# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_postnode_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('comment', models.CharField(max_length=255, verbose_name='Comment')),
                ('created_by', models.ForeignKey(related_name='created_blog_postrevision_set', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='modified_blog_postrevision_set', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(to='blog.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
