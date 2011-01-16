from django.core.management.base import BaseCommand, CommandError
from liberweb.serie import models as m

from django.conf import settings

from imdb import IMDb
from tvdb_api import Tvdb

from django.core.files.base import ContentFile
import urllib
import os.path
import datetime

import time

from optparse import make_option

from sys import stderr

def warn(msg):
    print >> stderr, msg

try:
    import json
except:
    import simplejson as json #Python 2.5 compability pypy

class Command(BaseCommand):
    args = '<json_file json_file ...>'
    help = 'Import bot data from generated json files'
    option_list = BaseCommand.option_list + (
        make_option('--bot',
            action='store',
            dest='bot',
            default="import_bot_data",
            help='Name of the importer bot'),
        )

    not_found = set()
    bot = None
    imdb = None

    def handle(self, *args, **options):
        self.bot = options.get("bot")
        imdb_am = settings.IMDB_ACCESS_SYSTEM
        if imdb_am == "http":
            self.imdb = IMDb()
        elif imdb_am == "sql":
            self.imdb = IMDb("sql", settings.IMDB_ACCESS_DB_URI)
        else:
            raise CommandError("Incorrect configuration of IMDB_ACCESS_SYSTEM property")

        for f in args:
            print "Importing...", f
            data = json.load(open(f))
            for link in data:
                print link
                #Data checks
                if "serie" not in link or link["serie"] in self.not_found:
                    warn("Problems looking up serie %s" % link)
                elif "temp" not in link or "epi" not in link:
                    warn("Season and episode is not setted in %s" % link)
                elif "lang" not in link:
                    warn(u"Serie %s with link %s has not lang" % (link["serie"], link["links"]))
                else:
                    try:
                        #Check if temp and epi are ints
                        link["temp"] = int(link["temp"])
                        link["epi"] = int(link["epi"])
                    except:
                        warn("Erroneous temp or epi in %s" % link)
                    else:
                        self.process_link(**link)
        print "List of series not found:"
        for serie in self.not_found:
            print "\t%s" % serie

    def process_link(self, epi=None, lang=None, links=None, serie=None,
            temp=None, type=None, title=None, sublink=None, sublang=None,
            **kw):
        if kw:
            warn(u"Unsuported fields in json: %s" % kw)
        try:
            db_link = m.Link.objects.get(url=links)
            db_link.audio_lang = self.normalize_lang(lang)
            db_link.subtitle = self.normalize_lang(sublang)
            db_link.user = self.bot
            db_link.save()
            return #It's already loaded, but update data
        except m.Link.DoesNotExist:
            try:
                db_serie_alias = m.SerieAlias.objects.get(name=serie)
                db_serie = db_serie_alias.serie
            except m.SerieAlias.DoesNotExist:
                #Normalize serie name in imdb
                normalized_serie = self.normalize_name(serie)
                if normalized_serie:
                    db_serie = self.populate_serie(normalized_serie, serie)
                    if not db_serie:
                        warn(u"%s is not found in tvdb" % normalized_serie)
                        self.not_found.add(serie)
                        return
                    db_serie.save()
                    db_serie_alias = m.SerieAlias()
                    db_serie_alias.serie = db_serie
                    db_serie_alias.name = serie
                    db_serie_alias.save()
                else:
                    warn(u"Not found serie '%s'" % serie)
                    self.not_found.add(serie)
                    return
        #Search episode in database
        try:
            db_season = self.populate_seasons(db_serie, temp)
            db_episode = m.Episode.objects.get(season=db_season, episode=epi)
        except m.Episode.DoesNotExist:
            warn(u"Episode %sx%s of %s not populated yet" % (temp, epi, serie))
            #Create episode
            db_episode = m.Episode()
            db_episode.serie = db_serie
            db_episode.title_en = db_episode.title_es = "%sx%s" % (temp, epi)
            db_episode.season = db_season
            db_episode.episode = int(epi)
            db_episode.description_en = "Not available"
            db_episode.description_es = "No disponible"
            db_episode.save()
            print "finalized importing episode, so what now?"

        db_lang = self.normalize_lang(lang)
        if not db_lang:
            warn(u"Invalid lang %s" % lang)
            return

        db_link = m.Link()
        db_link.episode = db_episode
        db_link.url = links
        db_link.audio_lang = self.normalize_lang(lang)
        db_link.subtitle = self.normalize_lang(sublang)
        db_link.bot = self.bot
        db_link.save()

    def normalize_name(self, name, retries=3):
        if retries:
            try:
                imdb_res = self.imdb.search_movie(name)
            except:
                time.sleep(30) #Wait 30secs and retry
                return self.normalize_name(name, retries-1)
            else:
                for res in imdb_res:
                    if res.get("kind", None) != "tv series":
                        continue
                    else:
                        return res["title"]
        return None


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
        if not lang_code:
            return None
        try:
            iso_code, country = langs[lang_code.lower()]
            return m.Languages.objects.get(iso_code=iso_code, country=country)
        except m.Languages.DoesNotExist:
            lang = m.Languages(iso_code=iso_code, country=country)
            lang.save()
            return lang
        except KeyError:
            pass
    
    def populate_serie(self, name, orig_name=None):
        tvdb_en = Tvdb(actors=True, banners=True)
        tvdb_es = Tvdb(language="es")
        try:
            reg_en = tvdb_en[name]
            reg_es = tvdb_es[name]
        except:
            try:
                reg_en = tvdb_en[orig_name]
                reg_es = tvdb_es[orig_name]
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

        #db_serie.rating = reg_en["rating"]
        #db_serie.rating_count = reg_en["ratingcount"]
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
            db_img.src.save(os.path.basename(reg_en["poster"]), file_content)
            db_img.save()

        for actor in reg_en["_actors"]:
            if not actor["name"]:
                continue #This field is needed
            db_actor = self.populate_actor(actor)
            db_role = m.Role(actor=db_actor, serie=db_serie, role=actor["role"] or "")
            try:
                db_role.save()
            except:
                continue

        self.populate_episodes(db_serie, reg_en, reg_es)

        return db_serie

    def populate_seasons(self, db_serie, ntemp):
        try:
            db_season = m.Season.objects.get(serie=db_serie, season=ntemp)
        except m.Season.DoesNotExist:
            db_season = m.Season()
            
        db_season.serie = db_serie
        db_season.season = int(ntemp)

        tvdb_en = Tvdb(actors=True, banners=True)
        reg_en = tvdb_en[db_serie.name]
     
        db_season.save()

        # seasonwide?
        if reg_en['_banners']['season']['season']:
            season_banners = reg_en['_banners']['season']['season']
            for img_banner in season_banners:
                if int(ntemp) == int(season_banners[img_banner]['season']):
                    img_url = season_banners[img_banner]['_bannerpath']
                    img_title = season_banners[img_banner]['id']
                    img = urllib.urlretrieve(img_url)
                    db_img = m.ImageSeason(is_poster=True, title=img_title)
                    db_img.season = db_season
                    file_content = ContentFile(open(img[0]).read())
                    db_img.src.save(os.path.basename(img_url), file_content)
                    db_img.save()
                    continue
        return db_season

    
#            if actor["image"]:
#                img = urllib.urlretrieve(actor["image"])
#                db_img = m.ImageActor(is_poster=True, title=actor["name"])
#                db_img.actor = db_actor
#                file_content = ContentFile(open(img[0]).read())
#                db_img.src.save(os.path.basename(actor["image"]), file_content)
#                db_img.save()
#            return db_actor

    def populate_episodes(self, db_serie, reg_en, reg_es):
        for n_season in reg_en:
            db_season = self.populate_seasons(db_serie, n_season)
            for n_episode in reg_en[n_season]:
                episode = reg_en[n_season][n_episode]
                try:
                    db_episode = m.Episode.objects.get(
                           # serie = db_serie,
                            season = db_season,
                            episode = n_episode,)
                except m.Episode.DoesNotExist:
                    db_episode = m.Episode()
                    db_episode.season = db_season
                    try:
                        db_episode.air_date = datetime.datetime.strptime(
                            episode["firstaired"], "%Y-%m-%d")
                    except:
                        db_episode.air_date = None
                    db_episode.title_en = reg_en[n_season][n_episode]["episodename"]
                    db_episode.episode = n_episode
                    db_episode.description_en = reg_en[n_season][n_episode]["overview"] or "Not available"
                    try:
                        db_episode.title_es = reg_es[n_season][n_episode]["episodename"]
                        db_episode.description_es = reg_es[n_season][n_episode]["overview"] or "No disponible"
                    except:
                        db_episode.title_es = "%sx%s" % (n_season, n_episode)
                        db_episode.description_es = "No disponible"
                    db_episode.save()
                    if reg_en[n_season][n_episode]["filename"]:
                        img = urllib.urlretrieve(reg_en[n_season][n_episode]["filename"])
                        db_img = m.ImageEpisode(is_poster=True, title=reg_es[n_season][n_episode]["episodename"])
                        db_img.episode = db_episode
                        file_content = ContentFile(open(img[0]).read())
                        db_img.src.save(os.path.basename(reg_en[n_season][n_episode]["filename"]), file_content)
                        db_img.save()


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
                #Genres need be traslated manually
                genre_db.name_en = genre_db.name_es = genre
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
