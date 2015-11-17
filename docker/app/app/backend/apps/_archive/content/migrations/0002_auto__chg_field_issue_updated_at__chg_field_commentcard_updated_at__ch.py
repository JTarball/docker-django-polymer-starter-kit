# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Issue.updated_at'
        db.alter_column(u'content_issue', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'CommentCard.updated_at'
        db.alter_column(u'content_commentcard', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Update.updated_at'
        db.alter_column(u'content_update', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Troubleshooting.updated_at'
        db.alter_column(u'content_troubleshooting', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Comment.updated_at'
        db.alter_column(u'content_comment', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Dependency.updated_at'
        db.alter_column(u'content_dependency', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Issue.updated_at'
        db.alter_column(u'content_issue', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'CommentCard.updated_at'
        db.alter_column(u'content_commentcard', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Update.updated_at'
        db.alter_column(u'content_update', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Troubleshooting.updated_at'
        db.alter_column(u'content_troubleshooting', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Comment.updated_at'
        db.alter_column(u'content_comment', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Dependency.updated_at'
        db.alter_column(u'content_dependency', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    models = {
        u'accounts.accountsuser': {
            'Meta': {'object_name': 'AccountsUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'content.category': {
            'Meta': {'ordering': "['-slug']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['content.Language']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'content.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']", 'null': 'True'}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.Comment']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.commentcard': {
            'Meta': {'object_name': 'CommentCard'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.PostCard']", 'null': 'True'}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.CommentCard']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']"}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.Dependency']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.genre': {
            'Meta': {'object_name': 'Genre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.Genre']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'content.issue': {
            'Meta': {'object_name': 'Issue'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']"}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.Issue']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.language': {
            'Meta': {'ordering': "['-slug']", 'object_name': 'Language'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'content.liker': {
            'Meta': {'object_name': 'Liker'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']"}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.PostCard']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'content.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_codeexamples': ('django.db.models.fields.TextField', [], {'default': "'code examples'", 'null': 'True', 'blank': 'True'}),
            'content_demo': ('django.db.models.fields.TextField', [], {'default': "'demo'", 'null': 'True', 'blank': 'True'}),
            'content_designdecisions': ('django.db.models.fields.TextField', [], {'default': "'design decisions'", 'null': 'True', 'blank': 'True'}),
            'content_furtherlearning': ('django.db.models.fields.TextField', [], {'default': "'further learning'", 'null': 'True', 'blank': 'True'}),
            'content_gotchas': ('django.db.models.fields.TextField', [], {'default': "'gotcha'", 'null': 'True', 'blank': 'True'}),
            'content_markdown': ('django.db.models.fields.TextField', [], {}),
            'content_markup': ('django.db.models.fields.TextField', [], {}),
            'content_trickstips': ('django.db.models.fields.TextField', [], {'default': "'trickstips'", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.PostNode']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'content.postcard': {
            'Meta': {'object_name': 'PostCard'},
            'brokens': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'null': 'True'}),
            'comments_pretty': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_at_pretty': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '50'}),
            'href': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_externalhref': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'likes_pretty': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'main_post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'views_pretty': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'})
        },
        u'content.postnode': {
            'Meta': {'object_name': 'PostNode'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.PostNode']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'content.subcategory': {
            'Meta': {'ordering': "['-slug']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['content.Category']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'content.troubleshooting': {
            'Meta': {'object_name': 'Troubleshooting'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']"}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.Troubleshooting']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.update': {
            'Meta': {'object_name': 'Update'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.AccountsUser']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ago': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Post']", 'null': 'True'}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postreply'", 'null': 'True', 'to': u"orm['content.Update']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content']