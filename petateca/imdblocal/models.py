# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class CharName(models.Model):
    name = models.TextField()
    imdb_index = models.CharField(max_length=12)
    imdb_id = models.IntegerField()
    name_pcode_nf = models.CharField(max_length=5)
    surname_pcode = models.CharField(max_length=5)
    class Meta:
        db_table = u'char_name'

class CompanyName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    country_code = models.CharField(max_length=255)
    imdb_id = models.IntegerField()
    name_pcode_nf = models.CharField(max_length=5)
    name_pcode_sf = models.CharField(max_length=5)
    class Meta:
        db_table = u'company_name'

class CompanyType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'company_type'

class CastInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    person = models.ForeignKey('Name')
    movie = models.ForeignKey('Title')
    person_role = models.ForeignKey('CharName')
    note = models.TextField()
    nr_order = models.IntegerField()
    role = models.ForeignKey('RoleType')
    class Meta:
        db_table = u'cast_info'

class CompCastType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'comp_cast_type'

class CompleteCast(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    subject = models.ForeignKey('CompCastType', related_name='subjects')
    status = models.ForeignKey('CompCastType', related_name='status')
    class Meta:
        db_table = u'complete_cast'

class InfoType(models.Model):
    id = models.IntegerField(primary_key=True)
    info = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'info_type'

class LinkType(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'link_type'

class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=255)
    phonetic_code = models.CharField(max_length=5)
    class Meta:
        db_table = u'keyword'

class MovieKeyword(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    keyword = models.ForeignKey('Keyword')
    class Meta:
        db_table = u'movie_keyword'

class MovieInfoIdx(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    info_type = models.ForeignKey('InfoType')
    info = models.TextField()
    note = models.TextField()
    class Meta:
        db_table = u'movie_info_idx'

class MovieCompanies(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    company = models.ForeignKey('CompanyName')
    company_type = models.ForeignKey('CompanyType')
    note = models.TextField()
    class Meta:
        db_table = u'movie_companies'

class PersonInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    person = models.ForeignKey('Name')
    info_type = models.ForeignKey('InfoType')
    info = models.TextField()
    note = models.TextField()
    class Meta:
        db_table = u'person_info'

class Title(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    imdb_index = models.CharField(max_length=12)
    kind = models.ForeignKey('KindType')
    production_year = models.IntegerField()
    imdb_id = models.IntegerField()
    phonetic_code = models.CharField(max_length=5)
    episode_of = models.ForeignKey('self', related_name='episodes')
    season_nr = models.IntegerField()
    episode_nr = models.IntegerField()
    series_years = models.CharField(max_length=49)
    class Meta:
        db_table = u'title'

class KindType(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(unique=True, max_length=15)
    class Meta:
        db_table = u'kind_type'

class AkaName(models.Model):
    id = models.IntegerField(primary_key=True)
    person = models.ForeignKey('Name')
    name = models.TextField()
    imdb_index = models.CharField(max_length=12)
    name_pcode_cf = models.CharField(max_length=5)
    name_pcode_nf = models.CharField(max_length=5)
    surname_pcode = models.CharField(max_length=5)
    class Meta:
        db_table = u'aka_name'

class Name(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    imdb_index = models.CharField(max_length=12)
    imdb_id = models.IntegerField()
    name_pcode_cf = models.CharField(max_length=5)
    name_pcode_nf = models.CharField(max_length=5)
    surname_pcode = models.CharField(max_length=5)
    class Meta:
        db_table = u'name'

class AkaTitle(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    title = models.TextField()
    imdb_index = models.CharField(max_length=12)
    kind = models.ForeignKey('KindType')
    production_year = models.IntegerField()
    phonetic_code = models.CharField(max_length=5)
    episode_of = models.ForeignKey('self')
    season_nr = models.IntegerField()
    episode_nr = models.IntegerField()
    note = models.TextField()
    class Meta:
        db_table = u'aka_title'

class RoleType(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'role_type'

class MovieLink(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title', related_name='movies')
    linked_movie = models.ForeignKey('Title', related_name='movies_links')
    link_type = models.ForeignKey('LinkType')
    class Meta:
        db_table = u'movie_link'

class MovieInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Title')
    info_type = models.ForeignKey('InfoType')
    info = models.TextField()
    note = models.TextField()
    class Meta:
        db_table = u'movie_info'

