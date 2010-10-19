# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Episode.title_en'
        db.add_column('serie_episode', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=255), keep_default=False)

        # Adding field 'Episode.title_es'
        db.add_column('serie_episode', 'title_es', self.gf('django.db.models.fields.CharField')(max_length=255), keep_default=False)

        # Adding field 'Episode.description_en'
        db.add_column('serie_episode', 'description_en', self.gf('django.db.models.fields.TextField')(), keep_default=False)

        # Adding field 'Episode.description_es'
        db.add_column('serie_episode', 'description_es', self.gf('django.db.models.fields.TextField')(), keep_default=False)

        # Adding field 'Serie.name_en'
        db.add_column('serie_serie', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255), keep_default=False)

        # Adding field 'Serie.name_es'
        db.add_column('serie_serie', 'name_es', self.gf('django.db.models.fields.CharField')(max_length=255), keep_default=False)

        # Adding field 'Serie.description_en'
        db.add_column('serie_serie', 'description_en', self.gf('django.db.models.fields.TextField')(), keep_default=False)

        # Adding field 'Serie.description_es'
        db.add_column('serie_serie', 'description_es', self.gf('django.db.models.fields.TextField')(), keep_default=False)

        # Adding field 'Genre.name_en'
        db.add_column('serie_genre', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=25), keep_default=False)

        # Adding field 'Genre.name_es'
        db.add_column('serie_genre', 'name_es', self.gf('django.db.models.fields.CharField')(max_length=25), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Episode.title_en'
        db.delete_column('serie_episode', 'title_en')

        # Deleting field 'Episode.title_es'
        db.delete_column('serie_episode', 'title_es')

        # Deleting field 'Episode.description_en'
        db.delete_column('serie_episode', 'description_en')

        # Deleting field 'Episode.description_es'
        db.delete_column('serie_episode', 'description_es')

        # Deleting field 'Serie.name_en'
        db.delete_column('serie_serie', 'name_en')

        # Deleting field 'Serie.name_es'
        db.delete_column('serie_serie', 'name_es')

        # Deleting field 'Serie.description_en'
        db.delete_column('serie_serie', 'description_en')

        # Deleting field 'Serie.description_es'
        db.delete_column('serie_serie', 'description_es')

        # Deleting field 'Genre.name_en'
        db.delete_column('serie_genre', 'name_en')

        # Deleting field 'Genre.name_es'
        db.delete_column('serie_genre', 'name_es')


    models = {
        'serie.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.episode': {
            'Meta': {'object_name': 'Episode'},
            'air_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_es': ('django.db.models.fields.TextField', [], {}),
            'episode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['serie.Serie']"}),
            'slug_title': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'serie.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'serie.imageactor': {
            'Meta': {'object_name': 'ImageActor'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['serie.Actor']"}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_poster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.imageserie': {
            'Meta': {'object_name': 'ImageSerie'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_poster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['serie.Serie']"}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.languages': {
            'Meta': {'object_name': 'Languages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        'serie.link': {
            'Meta': {'object_name': 'Link'},
            'audio_lang': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audio_langs'", 'to': "orm['serie.Languages']"}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['serie.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_langs'", 'null': 'True', 'to': "orm['serie.Languages']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'serie.network': {
            'Meta': {'object_name': 'Network'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'serie.serie': {
            'Meta': {'object_name': 'Serie'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['serie.Actor']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_es': ('django.db.models.fields.TextField', [], {}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'series'", 'symmetrical': 'False', 'to': "orm['serie.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series'", 'to': "orm['serie.Network']"}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'serie.subtitlelink': {
            'Meta': {'object_name': 'SubtitleLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serie.Languages']"}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtitles'", 'to': "orm['serie.Link']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['serie']
