# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Post.post_es'
        db.add_column('blog_post', 'post_es', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)

        # Adding field 'Post.title_en'
        db.add_column('blog_post', 'title_en', self.gf('django.db.models.fields.CharField')(null=True, max_length=64), keep_default=False)

        # Adding field 'Post.title_es'
        db.add_column('blog_post', 'title_es', self.gf('django.db.models.fields.CharField')(null=True, max_length=64), keep_default=False)

        # Adding field 'Post.post_en'
        db.add_column('blog_post', 'post_en', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Post.post_es'
        db.delete_column('blog_post', 'post_es')

        # Deleting field 'Post.title_en'
        db.delete_column('blog_post', 'title_en')

        # Deleting field 'Post.title_es'
        db.delete_column('blog_post', 'title_es')

        # Deleting field 'Post.post_en'
        db.delete_column('blog_post', 'post_en')
    
    
    models = {
        'blog.imagepost': {
            'Meta': {'object_name': 'ImagePost'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['blog.Post']"}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'blog.post': {
            'Meta': {'object_name': 'Post'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'post_en': ('django.db.models.fields.TextField', [], {}),
            'post_es': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }
    
    complete_apps = ['blog']
