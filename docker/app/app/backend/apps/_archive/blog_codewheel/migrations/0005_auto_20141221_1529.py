# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postrevision',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='versions',
            field=models.ManyToManyField(to='blog.PostRevision', blank=True),
            preserve_default=True,
        ),
    ]
