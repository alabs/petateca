# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Episode.serie'
        db.alter_column('serie_episode', 'serie_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serie.Season']))

        # Deleting field 'Link.bot'
        db.delete_column('serie_link', 'bot')

        # Adding field 'Link.user'
        db.add_column('serie_link', 'user', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Changing field 'Episode.serie'
        db.alter_column('serie_episode', 'serie_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serie.Serie']))

        # Adding field 'Link.bot'
        db.add_column('serie_link', 'bot', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'Link.user'
        db.delete_column('serie_link', 'user')


    models = {
        'serie.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
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
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['serie.Season']"}),
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
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
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
        'serie.imageepisode': {
            'Meta': {'object_name': 'ImageEpisode'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['serie.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_poster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'serie.imageseason': {
            'Meta': {'object_name': 'ImageSeason'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_poster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['serie.Season']"}),
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
            'Meta': {'unique_together': "(('iso_code', 'country'),)", 'object_name': 'Languages'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'serie.link': {
            'Meta': {'object_name': 'Link'},
            'audio_lang': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audio_langs'", 'to': "orm['serie.Languages']"}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['serie.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'subtitle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_langs'", 'null': 'True', 'to': "orm['serie.Languages']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'serie.linkseason': {
            'Meta': {'object_name': 'LinkSeason'},
            'audio_lang': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audio_langs_season'", 'to': "orm['serie.Languages']"}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['serie.Season']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'subtitle': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_langs_season'", 'null': 'True', 'to': "orm['serie.Languages']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'serie.network': {
            'Meta': {'object_name': 'Network'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
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
        'serie.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'season'", 'to': "orm['serie.Serie']"})
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
            'rating_user_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_user_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'serie.seriealias': {
            'Meta': {'object_name': 'SerieAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['serie.Serie']"})
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
