#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# LiberImport has several functions for creating Network, Genre, Language, Actor
# Serie, Episode and Link. It also has several Import for testing.
#

# Import Django Settings
#from django.core.management import setup_environ
#import settings
#setup_environ(settings)

class CreateNetwork(object):

    def __init__(self, network_name):
        self.network_name = network_name

    def create_network(self):
        ''' 
        Search Network, returns it. 
        If it doesn't exists, create it using the first url found in Google
        '''
        from serie.models import Network
        try: 
            n = Network.objects.get(name=self.network_name)
            return n 
        except Network.DoesNotExist:
            network_url = self.google_search(self.network_name)
            n = Network(name=self.network_name, url=network_url)
            n.save()
            return n 

    def google_search(self, search_term):
        ''' Search in Google, returns first URL '''
        import urllib
        import simplejson
        query = urllib.urlencode({'q' : search_term})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        url = results[0]['url']
        return url

class CreateGenre(object):
    
    def __init__(self, genre_name):
        self.genre_name = genre_name

    def create_genre(self):
        ''' 
        Search Genre, returns it. If it doesn't exists, create it.
        '''
        from serie.models import Genre
        try: 
            g = Genre.objects.get(name=self.genre_name)
        except Genre.DoesNotExist:
            g = Genre(name=self.genre_name)
            g.save()
        finally:
            return g 

class CreateLanguage(object):

    def __init__(self, lang_name):
        self.lang_name = lang_name
    
    def create_language(self):
        ''' 
        Search Language, returns isocode. If it doesn't exists, create it.
        '''
        from serie.models import Languages
        lang_iso=''
        if self.lang_name == 'Spanish' or 'Dual' or 'Latino':
            lang_iso = 'es'
        elif self.lang_name == 'English':
            lang_iso = 'en'
        try: 
            l = Languages.objects.get(iso_code=lang_iso)
            return l 
        except Languages.DoesNotExist:
            l = Languages(iso_code=lang_iso)
            l.save()
            return l 

class CreateActor(object):

    def __init__(self, actor_name):
        self.actor_name = actor_name

    def create_actor(self):
        ''' 
        Search Actor, returns it.
        If it doesn't exists, create it and his photos
        '''
        from serie.models import Actor, ImageActor
        try: 
            a = Actor.objects.get(name=self.actor_name)
            return a
        except Actor.DoesNotExist:
            a = Actor(name=self.actor_name)
        # TODO: ImageActor 
            a.save()
            return a

class CreateSerie(object):

    def __init__(self, serie_untrust):
        self.serie_untrust = serie_untrust

    def create_serie(self):
        '''
        Search for serie, returns it
        If it doesn't exists, creates Network, creates Serie and creates and add Genres
        TODO: Add actors and images
        '''
        from serie.models import Serie
        serie_name = self.normalizer(self.serie_untrust)
        try: 
            s = Serie.objects.get(name=serie_name)
            return s
        except Serie.DoesNotExist:
            serie = self.get_serie(serie_name)
            n = CreateNetwork(serie['network'])
            n = n.create_network()
            s = Serie(name=serie['name'], runtime=serie['runtime'], description=serie['description'], network=n)
            s.save()
            for genre in serie['genres']:
              g = CreateGenre(genre)
              g = g.create_genre()
              s.genres.add(g)
            for actor in serie['actors']:
              a = CreateActor(actor)
              a = a.create_actor()
              s.actors.add(a)
            # TODO: Images
            return s

    def swap_dictionary(self, original_dict):
        ''' Swap values/keys '''
        return dict([(v, k) for (k, v) in original_dict.iteritems()])
    
    def normalizer(self, serie_untrust): 
        '''
        Receives serie_untrust, ask to IMDB and get serie_name
        Normalize Lost, lost, Perdidos, perdidos
        '''
        from imdb import IMDb
        ia = IMDb()
        serie_name = ia.search_movie(serie_untrust)[0]['title']
        return serie_name
    
    def get_serie(self, serie_untrust):
        ''' 
        Receives a serie name, returns a dict with name, genres, description, 
        network, actors and runtime
        '''
        from thetvdb.tool import Tool
        t = Tool()
        serie_name = self.normalizer(serie_untrust) # normalize the name
        series_list = t.get_series(serie_name) # receives similar series list
        query = self.swap_dictionary(series_list) # swap key/value
        serie_id = query.get(serie_name) # getting the ID
        serie_info = t.get_serie_information(int(serie_id), 'es') # ask with ID
        serie = {}
        serie['name'] = serie_name 
        serie['genres'] = serie_info['genres']
        serie['description'] = serie_info['description']
        serie['network'] = serie_info['network']
        serie['actors'] = serie_info['actors']
        serie['runtime'] = serie_info['runtime']
        return serie

class CreateEpisode(object):

    def __init__(self, serie_name, n_temp, n_epi):
        self.serie_name = serie_name
        self.n_temp = n_temp
        self.n_epi = n_epi

    def create_episode(self):
        ''' 
        Search for episode, returns it. 
        If it doesn't exists, search for air date, description and title
        ''' 
        from serie.models import Episode
        s = CreateSerie(self.serie_name)
        s = s.create_serie()
        try: 
            e = Episode.objects.get(serie=s, season=self.n_temp, episode=self.n_epi)
            return e
        except Episode.DoesNotExist:
            # Ask for air_date, title and description to thetvdb
            # t.get_episode_info(serie_title, n_temp, n_epi)
            # FIXME: slug_title
            ident = self.serie_name + ' - S' + self.n_temp + 'E' + self.n_epi
            e = Episode(serie=s, air_date='2010-01-01', description='niceme', title=ident, season=self.n_temp, episode=self.n_epi)
            e.save()
            return e

class CreateLink(object):

    def __init__(self, serie, n_temp, n_epi, url, audio_lang):
        self.serie = serie
        self.n_temp = n_temp
        self.n_epi = n_epi
        self.url = url
        self.audio_lang = audio_lang

    def create_link(self):
        '''
        Search for link, returns it. 
        If it doesn't exists, create it. 
        ''' 
        from serie.models import Link
        e = CreateEpisode(self.serie, self.n_temp, self.n_epi)
        e = e.create_episode()
        try: 
            l = Link.objects.get(url=self.url)
            return l
        except Link.DoesNotExist:
            au = CreateLanguage(self.audio_lang)
            au = au.create_language()
            l = Link(episode=e, url=self.url, audio_lang=au)
            l.save()
            return l

    def create_link_sub(self, subtitle):
        self.subtitle = subtitle
        '''
        Search for link with subtitles embedded, returns it. 
        If it doesn't exists, create it. 
        ''' 
        from serie.models import Link
        e = CreateEpisode(self.serie, self.n_temp, self.n_epi)
        e = e.create_episode()
        try: 
            l = Link.objects.get(url=self.url)
            return l
        except Link.DoesNotExist:
            au = CreateLanguage(self.audio_lang)
            au = au.create_language()
            su = CreateLanguage(self.subtitle)
            su = su.create_language()
            l = Link(episode=e, url=self.url, audio_lang=au, subtitle=su)
            l.save()
            return l

class Import(object):

    def json_file(self, import_file):
        '''
        Receives a JSON dump file, CreateLink for all links in it.
        '''
        from json import loads
        all_items = loads(open(import_file).read())
        for item in all_items:
            print item['lang']
            l = CreateLink(item['serie'], item['temp'], item['epi'], item['links'], item['lang'])
            try:
                l.create_link_sub(item['sublang'])
            except:
                print item['serie']
                l.create_link()
 
    def json_letter_site(self, letter, site):
        '''
        Receives letter and site, process to get the JSON dump file, 
        process to CreateLink for all links on it.
        BUG: It is necessary to be in liberweb root project
        '''
        from json import loads
        from liberclass.askletter import AskLetter
        import_file, export_file = AskLetter(letter,site)
        all_items = loads(open('bots/libercopy/' + export_file).read())
        for item in all_items:
            l = CreateLink(item['serie'], item['temp'], item['epi'], item['links'], item['lang'])
            l.create_link()
    
    def series_list(self, file):
        '''
        Receives a file with a series list and create them
        '''
        f = open(file)
        series = f.readlines()
        for serie in series:
            try:
                print serie.strip() + ' - OK'
                c = CreateSerie(serie.strip())
                c.create_serie()
                pass
            except:
                print serie.strip() + ' - NOT INSERTED'
                pass

