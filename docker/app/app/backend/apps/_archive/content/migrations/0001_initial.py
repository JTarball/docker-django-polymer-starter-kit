# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genre'
        db.create_table(u'content_genre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['content.Genre'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'content', ['Genre'])

        # Adding model 'Language'
        db.create_table(u'content_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'content', ['Language'])

        # Adding model 'Category'
        db.create_table(u'content_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'content', ['Category'])

        # Adding M2M table for field language on 'Category'
        m2m_table_name = db.shorten_name(u'content_category_language')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm[u'content.category'], null=False)),
            ('language', models.ForeignKey(orm[u'content.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['category_id', 'language_id'])

        # Adding model 'SubCategory'
        db.create_table(u'content_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'content', ['SubCategory'])

        # Adding M2M table for field category on 'SubCategory'
        m2m_table_name = db.shorten_name(u'content_subcategory_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subcategory', models.ForeignKey(orm[u'content.subcategory'], null=False)),
            ('category', models.ForeignKey(orm[u'content.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subcategory_id', 'category_id'])

        # Adding model 'PostNode'
        db.create_table(u'content_postnode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['content.PostNode'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'content', ['PostNode'])

        # Adding model 'Post'
        db.create_table(u'content_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_markdown', self.gf('django.db.models.fields.TextField')()),
            ('content_markup', self.gf('django.db.models.fields.TextField')()),
            ('content_codeexamples', self.gf('django.db.models.fields.TextField')(default='code examples', null=True, blank=True)),
            ('content_designdecisions', self.gf('django.db.models.fields.TextField')(default='design decisions', null=True, blank=True)),
            ('content_furtherlearning', self.gf('django.db.models.fields.TextField')(default='further learning', null=True, blank=True)),
            ('content_demo', self.gf('django.db.models.fields.TextField')(default='demo', null=True, blank=True)),
            ('content_gotchas', self.gf('django.db.models.fields.TextField')(default='gotcha', null=True, blank=True)),
            ('content_trickstips', self.gf('django.db.models.fields.TextField')(default='trickstips', null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.PostNode'], null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'content', ['Post'])

        # Adding model 'PostCard'
        db.create_table(u'content_postcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('likes', self.gf('django.db.models.fields.BigIntegerField')(default=0, null=True, blank=True)),
            ('views', self.gf('django.db.models.fields.BigIntegerField')(default=0, null=True, blank=True)),
            ('likes_pretty', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('views_pretty', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('comments_pretty', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('created_at_pretty', self.gf('django.db.models.fields.CharField')(default=0, max_length=50)),
            ('is_externalhref', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('href', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('brokens', self.gf('django.db.models.fields.BigIntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'content', ['PostCard'])

        # Adding model 'Liker'
        db.create_table(u'content_liker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.PostCard'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'])),
            ('liked_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['Liker'])

        # Adding model 'Comment'
        db.create_table(u'content_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.Comment'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'], null=True)),
        ))
        db.send_create_signal(u'content', ['Comment'])

        # Adding model 'CommentCard'
        db.create_table(u'content_commentcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.CommentCard'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.PostCard'], null=True)),
        ))
        db.send_create_signal(u'content', ['CommentCard'])

        # Adding model 'Update'
        db.create_table(u'content_update', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.Update'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'], null=True)),
        ))
        db.send_create_signal(u'content', ['Update'])

        # Adding model 'Issue'
        db.create_table(u'content_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.Issue'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'])),
        ))
        db.send_create_signal(u'content', ['Issue'])

        # Adding model 'Troubleshooting'
        db.create_table(u'content_troubleshooting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.Troubleshooting'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'])),
        ))
        db.send_create_signal(u'content', ['Troubleshooting'])

        # Adding model 'Dependency'
        db.create_table(u'content_dependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.AccountsUser'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_ago', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reply', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='postreply', null=True, to=orm['content.Dependency'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Post'])),
        ))
        db.send_create_signal(u'content', ['Dependency'])


    def backwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table(u'content_genre')

        # Deleting model 'Language'
        db.delete_table(u'content_language')

        # Deleting model 'Category'
        db.delete_table(u'content_category')

        # Removing M2M table for field language on 'Category'
        db.delete_table(db.shorten_name(u'content_category_language'))

        # Deleting model 'SubCategory'
        db.delete_table(u'content_subcategory')

        # Removing M2M table for field category on 'SubCategory'
        db.delete_table(db.shorten_name(u'content_subcategory_category'))

        # Deleting model 'PostNode'
        db.delete_table(u'content_postnode')

        # Deleting model 'Post'
        db.delete_table(u'content_post')

        # Deleting model 'PostCard'
        db.delete_table(u'content_postcard')

        # Deleting model 'Liker'
        db.delete_table(u'content_liker')

        # Deleting model 'Comment'
        db.delete_table(u'content_comment')

        # Deleting model 'CommentCard'
        db.delete_table(u'content_commentcard')

        # Deleting model 'Update'
        db.delete_table(u'content_update')

        # Deleting model 'Issue'
        db.delete_table(u'content_issue')

        # Deleting model 'Troubleshooting'
        db.delete_table(u'content_troubleshooting')

        # Deleting model 'Dependency'
        db.delete_table(u'content_dependency')


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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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