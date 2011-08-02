# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Book'
        db.create_table('book_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('isbn', self.gf('django.db.models.fields.IntegerField')()),
            ('poster', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='poster_of', unique=True, null=True, to=orm['book.ImageBook'])),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('book', ['Book'])

        # Adding M2M table for field category on 'Book'
        db.create_table('book_book_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['book.book'], null=False)),
            ('category', models.ForeignKey(orm['book.category'], null=False))
        ))
        db.create_unique('book_book_category', ['book_id', 'category_id'])

        # Adding M2M table for field author on 'Book'
        db.create_table('book_book_author', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['book.book'], null=False)),
            ('author', models.ForeignKey(orm['book.author'], null=False))
        ))
        db.create_unique('book_book_author', ['book_id', 'author_id'])

        # Adding model 'Category'
        db.create_table('book_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('book', ['Category'])

        # Adding model 'ImageBook'
        db.create_table('book_imagebook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('is_poster', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['book.Book'])),
        ))
        db.send_create_signal('book', ['ImageBook'])

        # Adding model 'BookLink'
        db.create_table('book_booklink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['book.Book'])),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(related_name='langs', to=orm['book.BookLanguages'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('check_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('book', ['BookLink'])

        # Adding model 'Author'
        db.create_table('book_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='books', to=orm['book.Book'])),
        ))
        db.send_create_signal('book', ['Author'])

        # Adding model 'BookLanguages'
        db.create_table('book_booklanguages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('book', ['BookLanguages'])

        # Adding unique constraint on 'BookLanguages', fields ['iso_code', 'country']
        db.create_unique('book_booklanguages', ['iso_code', 'country'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BookLanguages', fields ['iso_code', 'country']
        db.delete_unique('book_booklanguages', ['iso_code', 'country'])

        # Deleting model 'Book'
        db.delete_table('book_book')

        # Removing M2M table for field category on 'Book'
        db.delete_table('book_book_category')

        # Removing M2M table for field author on 'Book'
        db.delete_table('book_book_author')

        # Deleting model 'Category'
        db.delete_table('book_category')

        # Deleting model 'ImageBook'
        db.delete_table('book_imagebook')

        # Deleting model 'BookLink'
        db.delete_table('book_booklink')

        # Deleting model 'Author'
        db.delete_table('book_author')

        # Deleting model 'BookLanguages'
        db.delete_table('book_booklanguages')


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'books'", 'to': "orm['book.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'authors'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['book.Author']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'symmetrical': 'False', 'to': "orm['book.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'poster': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'poster_of'", 'unique': 'True', 'null': 'True', 'to': "orm['book.ImageBook']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'book.booklanguages': {
            'Meta': {'unique_together': "(('iso_code', 'country'),)", 'object_name': 'BookLanguages'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'book.booklink': {
            'Meta': {'object_name': 'BookLink'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['book.Book']"}),
            'check_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'langs'", 'to': "orm['book.BookLanguages']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'book.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'book.imagebook': {
            'Meta': {'object_name': 'ImageBook'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['book.Book']"}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_poster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['book']
