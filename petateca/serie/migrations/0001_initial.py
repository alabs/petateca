# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Serie'
        db.create_table('serie_serie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(related_name='series', to=orm['serie.Network'])),
            ('runtime', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('serie', ['Serie'])

        # Adding M2M table for field genres on 'Serie'
        db.create_table('serie_serie_genres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('serie', models.ForeignKey(orm['serie.serie'], null=False)),
            ('genre', models.ForeignKey(orm['serie.genre'], null=False))
        ))
        db.create_unique('serie_serie_genres', ['serie_id', 'genre_id'])

        # Adding M2M table for field actors on 'Serie'
        db.create_table('serie_serie_actors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('serie', models.ForeignKey(orm['serie.serie'], null=False)),
            ('actor', models.ForeignKey(orm['serie.actor'], null=False))
        ))
        db.create_unique('serie_serie_actors', ['serie_id', 'actor_id'])

        # Adding model 'Episode'
        db.create_table('serie_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodes', to=orm['serie.Serie'])),
            ('air_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug_title', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('season', self.gf('django.db.models.fields.IntegerField')()),
            ('episode', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified_time', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('serie', ['Episode'])

        # Adding model 'Link'
        db.create_table('serie_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['serie.Episode'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('audio_lang', self.gf('django.db.models.fields.related.ForeignKey')(related_name='audio_langs', to=orm['serie.Languages'])),
            ('subtitle', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_langs', null=True, to=orm['serie.Languages'])),
        ))
        db.send_create_signal('serie', ['Link'])

        # Adding model 'SubtitleLink'
        db.create_table('serie_subtitlelink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['serie.Languages'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtitles', to=orm['serie.Link'])),
        ))
        db.send_create_signal('serie', ['SubtitleLink'])

        # Adding model 'Languages'
        db.create_table('serie_languages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal('serie', ['Languages'])

        # Adding model 'Network'
        db.create_table('serie_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('serie', ['Network'])

        # Adding model 'Genre'
        db.create_table('serie_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('serie', ['Genre'])

        # Adding model 'Actor'
        db.create_table('serie_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('serie', ['Actor'])

        # Adding model 'ImageSerie'
        db.create_table('serie_imageserie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('is_poster', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('serie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['serie.Serie'])),
        ))
        db.send_create_signal('serie', ['ImageSerie'])

        # Adding model 'ImageActor'
        db.create_table('serie_imageactor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('is_poster', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['serie.Actor'])),
        ))
        db.send_create_signal('serie', ['ImageActor'])


    def backwards(self, orm):
        
        # Deleting model 'Serie'
        db.delete_table('serie_serie')

        # Removing M2M table for field genres on 'Serie'
        db.delete_table('serie_serie_genres')

        # Removing M2M table for field actors on 'Serie'
        db.delete_table('serie_serie_actors')

        # Deleting model 'Episode'
        db.delete_table('serie_episode')

        # Deleting model 'Link'
        db.delete_table('serie_link')

        # Deleting model 'SubtitleLink'
        db.delete_table('serie_subtitlelink')

        # Deleting model 'Languages'
        db.delete_table('serie_languages')

        # Deleting model 'Network'
        db.delete_table('serie_network')

        # Deleting model 'Genre'
        db.delete_table('serie_genre')

        # Deleting model 'Actor'
        db.delete_table('serie_actor')

        # Deleting model 'ImageSerie'
        db.delete_table('serie_imageserie')

        # Deleting model 'ImageActor'
        db.delete_table('serie_imageactor')


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
            'episode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['serie.Serie']"}),
            'slug_title': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'serie.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'series'", 'symmetrical': 'False', 'to': "orm['serie.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
