# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('userdata_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('userdata', ['UserProfile'])

        # Adding M2M table for field favorite_series on 'UserProfile'
        db.create_table('userdata_userprofile_favorite_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['userdata.userprofile'], null=False)),
            ('serie', models.ForeignKey(orm['serie.serie'], null=False))
        ))
        db.create_unique('userdata_userprofile_favorite_series', ['userprofile_id', 'serie_id'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('userdata_userprofile')

        # Removing M2M table for field favorite_series on 'UserProfile'
        db.delete_table('userdata_userprofile_favorite_series')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'serie.network': {
            'Meta': {'object_name': 'Network'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'serie.role': {
            'Meta': {'unique_together': "(('serie', 'actor', 'role'),)", 'object_name': 'Role'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serie.Actor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serie.Serie']"}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'serie.serie': {
            'Meta': {'object_name': 'Serie'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['serie.Actor']", 'through': "orm['serie.Role']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_es': ('django.db.models.fields.TextField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'series'", 'symmetrical': 'False', 'to': "orm['serie.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series'", 'to': "orm['serie.Network']"}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'userdata.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'favorite_series': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'favorite_of'", 'symmetrical': 'False', 'to': "orm['serie.Serie']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['userdata']
