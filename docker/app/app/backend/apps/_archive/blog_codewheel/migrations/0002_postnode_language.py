# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postnode',
            name='language',
            field=mptt.fields.TreeForeignKey(blank=True, to='blog.PostNode', null=True),
            preserve_default=True,
        ),
    ]
