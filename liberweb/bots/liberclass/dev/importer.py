#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Scrapy -> Django conversor
#

# Import Django Settings
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Import Django Models
#from serie.models import Actor, Episode, ImageActor, ImageSerie, Languages, Link, Serie

def google_search(search_term):
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

def check_and_import_network(name):
    ''' 
    Search Network, returns it. 
    If it doesn't exists, create it using the first url found in Google
    '''
    from serie.models import Network
    try: 
        n = Network.objects.get(name=name)
    except Network.DoesNotExist:
        network_url = google_search(name)
        n = Network(name=name, url=network_url)
        n.save()
    finally:
        return n 

def check_and_import_genres(name):
    ''' 
    Search Genre, returns it. If it doesn't exists, create it.
    '''
    from serie.models import Genre
    try: 
        g = Genre.objects.get(name=name)
    except Genre.DoesNotExist:
        g = Genre(name=name)
        g.save()
    finally:
        return g 

def check_and_import_language(lang_name):
    ''' 
    Search Language, returns isocode. If it doesn't exists, create it.
    '''
    from serie.models import Languages
    if lang_name == 'Spanish':
        lang_iso = 'es'
    elif lang_name == 'English':
        lang_iso = 'en'
    try: 
        l = Languages.objects.get(iso_code=lang_iso)
    except Languages.DoesNotExist:
        l = Languages(iso_code=lang_iso)
        l.save()
    finally:
        return l 

def check_and_import_actors(actor_name):
    ''' 
    Search Actor, returns it.
    If it doesn't exists, create it and his photos
    '''
    from serie.models import Actor, ImageActor
    try: 
        a = Actor.objects.get(name=actor_name)
    except Actor.DoesNotExist:
        a = Actor(name=actor_name)
    # TODO: ImageActor 
        a.save()
    finally:
        return a

def check_and_import_serie(name):
    '''
    Search for serie, returns it
    If it doesn't exists, creates Network, creates Serie and creates and add Genres
    TODO: Add actors and images
    '''
    from serie.models import Serie
    serie_name = normalizer(name)
    try: 
        s = Serie.objects.get(name=serie_name)
        return s
    except Serie.DoesNotExist:
        serie = get_serie(name)
        n = check_and_import_network(serie['network'])
        s = Serie(name=serie['name'], runtime=serie['runtime'], network=n, description=serie['description'])
        s.save()
        for genre in serie['genres']:
          g = check_and_import_genres(genre)
          s.genres.add(g)
        for actor in serie['actors']:
          a = check_and_import_actors(actor)
          s.actors.add(a)
        # TODO: Images
        return s

def check_and_import_episode(serie_name, n_temp, n_epi):
    ''' 
    Search for episode, returns it. 
    If it doesn't exists, search for air date, description and title
    ''' 
    from serie.models import Episode
    s = check_and_import_serie(serie_name)
    try: 
        e = Episode.objects.get(serie=s, season=n_temp, episode=n_epi)
        return e
    except Episode.DoesNotExist:
        # Ask for air_date, title and description to thetvdb
        # t.get_episode_info(serie_title, n_temp, n_epi)
        # FIXME: slug_title
        ident = serie_name + ' - S' + n_temp + 'E' + n_epi
        e = Episode(serie=s, air_date='2010-01-01', description='niceme', title=ident, season=n_temp, episode=n_epi)
        e.save()
        return e

def check_and_import_links_sub(serie, n_temp, n_epi, url, audio_lang, subtitle):
    '''
    Search for link with subtitles embedded, returns it. 
    If it doesn't exists, create it. 
    ''' 
    from serie.models import Link
    e = check_and_import_episode(serie, n_temp, n_epi)
    try: 
        l = Link.objects.get(url=url)
        return l
    except Link.DoesNotExist:
        au = check_and_import_language(audio_lang)
        su = check_and_import_language(subtitle)
        l = Link(episode=e, url=url, audio_lang=au, subtitle=su)
        l.save()
        return l

def check_and_import_links(serie, n_temp, n_epi, url, audio_lang):
    '''
    Search for link, returns it. 
    If it doesn't exists, create it. 
    ''' 
    from serie.models import Link
    e = check_and_import_episode(serie, n_temp, n_epi)
    try: 
        l = Link.objects.get(url=url)
        return l
    except Link.DoesNotExist:
        au = check_and_import_language(audio_lang)
        l = Link(episode=e, url=url, audio_lang=au)
        l.save()
        return l

def swap_dictionary(original_dict):
    ''' Swap values/keys '''
    return dict([(v, k) for (k, v) in original_dict.iteritems()])

def normalizer(serie_untrust): 
    '''
    Receives serie_untrust, ask to IMDB and get serie_name
    Normalize Lost, lost, Perdidos, perdidos
    '''
    from imdb import IMDb
    ia = IMDb()
    serie_name = ia.search_movie(serie_untrust)[0]['title']
    return serie_name

def get_serie(serie_untrust):
    ''' 
    Receives a serie name, returns a dict with name, genres, description, 
    network, actors and runtime
    '''
    from thetvdb.tool import Tool
    t = Tool()
    serie_name = normalizer(serie_untrust) # normalize the name
    series_list = t.get_series(serie_name) # receives similar series list
    query = swap_dictionary(series_list) # swap key/value
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

def test_import_json_letter(letter,site):
    '''
    Receives letter and site, process to get the JSON dump file, 
    returns all JSON items in that file. 
    '''
    from json import loads
    from liberclass.askletter import AskLetter
    import_file, export_file = AskLetter(letter,site)
    all_items = loads(open('bots/libercopy/' + export_file).read())
    return all_items

def test_import_letter(letter, site):
    '''
    Receives letter and site, process to get the JSON dump file, 
    process to get all the links to LiberWeb 
    '''
    all_items = test_import_json_letter(letter,site)
    for item in all_items:
        ## These are the items we got so far: 
        ## item['serie'], item['temp'], item['epi'], item['type'], item['links'], item['lang'], link_sublang = item['sublang']
        ## So first we should check if the Serie (TV Show) exists:
        # check_and_import_serie(item['serie'])
        ## Then we check if the Episode exists:
        #check_and_import_episode(item['temp'])
        # Finally we can the check and import the link
        check_and_import_links(item['serie'], item['temp'], item['epi'], item['links'], item['lang'])

def test_import_series_list(file):
    '''
    Receives a file with a series list and create them
    '''
    f = open(file)
    series = f.readlines()
    for serie in series:
        try:
            print serie.strip() + ' - OK'
            check_and_import_serie(serie.strip())
            pass
        except:
            print serie.strip() + ' - NOT INSERTED'
            pass

