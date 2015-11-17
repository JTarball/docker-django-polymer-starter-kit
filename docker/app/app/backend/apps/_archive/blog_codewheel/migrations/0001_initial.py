# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Comment'), (2, b'Issues'), (3, b'Troubleshooting'), (4, b'Updates'), (5, b'Code Examples')])),
                ('content', models.TextField(default=b'this is the default comment.')),
                ('idname', models.CharField(max_length=8)),
                ('is_reply', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('reply', models.ForeignKey(related_name='commentreply', blank=True, to='blog.Comment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('content', models.TextField(default=b'this is the default content.')),
                ('content_markup', models.TextField(help_text=' ', verbose_name='Content (Markdown)', blank=True)),
                ('update_comment', models.CharField(max_length=255, verbose_name='Commit Comment')),
                ('update_major', models.BooleanField(default=True)),
                ('comments', models.ManyToManyField(help_text=b'If you save here - the normal save will be overridden by save_related in the adminModel', to='blog.Comment', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(help_text=' ', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='blog.PostNode', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'vtag',
                'verbose_name_plural': 'vtags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='exclude_tags',
            field=models.ManyToManyField(related_name='exclude_tags', to='blog.VirtualTag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='include_tags',
            field=models.ManyToManyField(related_name='include_tags', to='blog.VirtualTag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='node',
            field=models.ForeignKey(blank=True, to='blog.PostNode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
