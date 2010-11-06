from django.core.management.base import BaseCommand, CommandError
from liberweb.serie import models as m

from django.conf import settings

from warnings import warn

from collections import defaultdict

from imdb import IMDb
from tvdb_api import Tvdb

from django.core.files.base import ContentFile
import urllib
import os.path
import datetime

try:
    import json
except:
    import simplejson as json #Python 2.5 compability pypy

class Command(BaseCommand):
    args = '<json_file json_file ...>'
    help = 'Import bot data from generated json files'

    def handle(self, *args, **options):
        imdb_am = settings.IMDB_ACCESS_SYSTEM
        if imdb_am == "http":
            self.imdb = IMDb()
        elif imdb_am == "sql":
            self.imdb = IMDb("sql", settings.IMDB_ACCESS_DB_URI)
        else:
            raise CommandError("Incorrect configuration of IMDB_ACCESS_SYSTEM property")

        for file in args:
            print "Importing...", file
            data = json.load(open(file))
            for link in data:
                print link
                if not link["temp"] or not link["epi"]:
                    warn("Season and episode is not setted")
                    continue
                self.process_link(**link)

    def process_link(self, epi=None, lang=None, links=None, serie=None,
            temp=None, type=None, title=None, sublink=None, sublang=None,
            **kw):
        if kw:
            warn("Unsuported fields in json: %s" % kw)
        if not lang:
            warn("Serie %s with link %s has not lang" % (serie, links))
            return
        try:
            m.Link.objects.get(url=links)
            return #It's already loaded
        except m.Link.DoesNotExist:
            pass

        try:
            db_serie_alias = m.SerieAlias.objects.get(name=serie)
            db_serie = db_serie_alias.serie
        except m.SerieAlias.DoesNotExist:
            #Normalize serie name in imdb
            imdb_res = self.imdb.search_movie(serie)
            imdb_reg = None
            for res in imdb_res:
                if res["kind"] != "tv series":
                    continue
                else:
                    imdb_reg = res
                    break
            if imdb_reg:
                db_serie = self.populate_serie(imdb_reg["title"])
                if not db_serie:
                    warn("%s is not found in tvdb" % imdb_reg["title"])
                    return
                db_serie.save()
                db_serie_alias = m.SerieAlias()
                db_serie_alias.serie = db_serie
                db_serie_alias.name = serie
                db_serie_alias.save()
            else:
                warn("Not found serie '%s'" % serie)
                return
        #Search episode in database
        try:
            db_episode = m.Episode.objects.get(serie=db_serie, season=temp, episode=epi)
        except m.Episode.DoesNotExist:
            warn("Episode %sx%s of %s not populated yet" % (temp, epi, serie))
            #Create episode
            db_episode = m.Episode()
            db_episode.serie = db_serie
            db_episode.title_en = db_episode.title_es = "%sx%s" % (temp, epi)
            db_episode.season = int(temp)
            db_episode.episode = int(epi)
            db_episode.description_en = "Not available"
            db_episode.description_es = "No disponible"
            db_episode.save()

        db_lang = self.normalize_lang(lang)
        if not db_lang:
            warn("Invalid lang %s" % lang)
            return
        db_link = m.Link()
        db_link.episode = db_episode
        db_link.url = links
        db_link.audio_lang = self.normalize_lang(lang)
        #TODO: Subtitle stuff
        db_link.save()

    def normalize_lang(self, lang_code):
        langs = {
            "spanish": ("es", "es"),
            "japanese": ("jp", None),
            "latin": ("es", None),
            "english": ("en", None),
            "es-es": ("es", "es"),
            "jp": ("jp", None),
            "es": ("es", None),
            "en": ("en", None),
        }
        try:
            iso_code, country = langs[lang_code.lower()]
            return m.Languages.objects.get(iso_code=iso_code, country=country)
        except m.Languages.DoesNotExist:
            lang = m.Languages(iso_code=iso_code, country=country)
            lang.save()
            return lang
        except KeyError:
            pass
    
    def populate_serie(self, name):
        tvdb_en = Tvdb(actors=True, banners=True)
        tvdb_es = Tvdb(language="es")
        try:
            reg_en = tvdb_en[name]
            reg_es = tvdb_es[name]
        except:
            return None
        
        try:
            db_serie = m.Serie.objects.get(name=name)
        except m.Serie.DoesNotExist:
            db_serie = m.Serie()

        db_serie.name = name
        db_serie.name_en = reg_en["seriesname"]
        db_serie.name_es = reg_es["seriesname"]
        
        if reg_en["network"]:
            db_serie.network = self.populate_network(reg_en["network"])

        db_serie.rating = reg_en["rating"]
        db_serie.rating_count = reg_en["ratingcount"]
        db_serie.runtime = reg_en["runtime"]

        db_serie.description_en = reg_en["overview"]
        db_serie.description_es = reg_es["overview"]

        db_serie.finished = reg_en["status"] == "Ended"

        db_serie.save()

        for genre in self.populate_genres(reg_en["genre"]):
            db_serie.genres.add(genre)

        if reg_en["poster"]:
            img = urllib.urlretrieve(reg_en["poster"])
            db_img = m.ImageSerie(is_poster=True, title=reg_en["seriesname"])
            db_img.serie = db_serie
            file_content = ContentFile(open(img[0]).read())
            db_img.src.save(os.path.basename(reg_en["poster"]),file_content)
            db_img.save()

        for actor in reg_en["_actors"]:
            db_actor = self.populate_actor(actor)
            db_role = m.Role(actor=db_actor, serie=db_serie, role=actor["role"] or "")
            db_role.save()

        self.populate_episodes(db_serie, reg_en, reg_es)

        return db_serie


    def populate_episodes(self, db_serie, reg_en, reg_es):
        for n_season in reg_en:
            for n_episode in reg_en[n_season]:
                episode = reg_en[n_season][n_episode]
                try:
                    db_episode = m.Episode.objects.get(
                            serie = db_serie,
                            season = n_season,
                            episode = n_episode,)
                except m.Episode.DoesNotExist:
                    db_episode = m.Episode()
                    db_episode.serie = db_serie
                    db_episode.air_date = datetime.datetime.strptime(
                            episode["firstaired"], "%Y-%m-%d") if episode["firstaired"] else None
                    db_episode.title_en = reg_en[n_season][n_episode]["episodename"]
                    db_episode.title_es = reg_es[n_season][n_episode]["episodename"]
                    db_episode.season = n_season
                    db_episode.episode = n_episode
                    db_episode.description_en = reg_en[n_season][n_episode]["overview"] or "Not available"
                    db_episode.description_es = reg_es[n_season][n_episode]["overview"] or "No disponible"
                    db_episode.save()

    def populate_network(self, network):
        try:
            return m.Network.objects.get(name=network)
        except m.Network.DoesNotExist:
            network_db = m.Network(name=network)
            network_db.save()
            return network_db

    def populate_genres(self, genres_str):
        def get_or_create(genre):
            try:
                return m.Genre.objects.get(name_en=genre)
            except m.Genre.DoesNotExist:
                genre_db = m.Genre()
                genre_db.name_en = genre_db.name_es = genre #XXX: Genres need traslation
                genre_db.save()
                return genre_db
        if not genres_str:
            return []
        return [get_or_create(genre) for genre in genres_str.split("|") if genre]


    def populate_actor(self, actor):
        try:
            return m.Actor.objects.get(name=actor["name"])
        except m.Actor.DoesNotExist:
            db_actor = m.Actor( name=actor["name"] )
            db_actor.save()
            if actor["image"]:
                img = urllib.urlretrieve(actor["image"])
                db_img = m.ImageActor(is_poster=True, title=actor["name"])
                db_img.actor = db_actor
                file_content = ContentFile(open(img[0]).read())
                db_img.src.save(os.path.basename(actor["image"]), file_content)
                db_img.save()
            return db_actor
