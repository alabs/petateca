# encoding: utf-8
"""
Tests para la APP de serie
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User

from serie import models as m

from serie.templatetags.background_color import background_color
from serie.templatetags.echo_language import echo_language 
from serie.templatetags.extract_domain import extract_domain
from serie.templatetags.extract_type import extract_type
from serie.templatetags.tagcloud import tagcloud

from voting.models import Vote


class SerieTest(TestCase):
    fixtures = ['twin_peaks.json']
    
    # GETS
    def GET(self, url, status=200):
        '''
        Get a URL and require a specific status code before proceeding
        http://djangosnippets.org/snippets/137/
        '''
        self.client = Client()
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, status)
        return response

    def test_serie_list(self):
        ''' Listado de series '''
        self.GET('/series/')

    def test_serie_lookup(self):
        ''' Las burbujas con la info de la serie '''
        self.GET('/series/lookup/serie/1/')

    def test_lookup_genre(self):
        ''' Genero en el listado de series '''
        self.GET('/series/lookup/genre/drama/')

    def test_lookup_genre_404(self):
        ''' Genero no encontrado en el listado de series '''
        self.GET('/series/lookup/genre/genero-no-existente/', status=404)

    def test_lookup_network(self):
        ''' Cadena en el listado de series '''
        self.GET('/series/lookup/network/abc/')

    def test_lookup_network_404(self):
        ''' Cadena no encontrada en el listado de series '''
        self.GET('/series/lookup/network/network-no-existente/', status=404)

    def test_get_serie(self):
        ''' Ficha de la serie '''
        self.GET('/serie/twin-peaks/')

    def test_get_serie_404(self):
        ''' Ficha de serie que no existe '''
        self.GET('/serie/esta-serie-no-existe/', status=404)

    def test_get_season(self):
        ''' Ver temporada de una serie '''
        self.GET('/series/lookup/serie/1/season/2/')

    def test_get_episode(self):
        ''' Ver episodio de una serie '''
        self.GET('/series/links/list/1/1/1/')

    def test_get_episode_description(self):
        ''' Ver descripcion episodio de una serie '''
        self.GET('/series/lookup/espoiler/1/1/1/')

    def test_get_all_actors(self):
        ''' Ver actores de una serie '''
        self.GET('/series/lookup/actors/twin-peaks/')

    def test_get_actor(self):
        ''' Ver actor '''
        self.GET('/series/actor/heather-graham/')

    # REDIRECTS

    def test_get_form_add_season(self):
        '''
        Recibir el formulario de agregar temporada 
        '''
        self.GET('/serie/twin-peaks/add/', status=302)

    def test_get_form_add_episode(self):
        '''
        Recibir el formulario de agregar episodio
        '''
        self.GET('/series/lookup/serie/1/season/1/add/episode/', status=302)

    def test_get_form_add_link(self):
        '''
        Recibiendo el formulario de agregar link
        '''
        self.GET('/series/links/add/episode/100/', status=302)

    # POST
    # Formularios para usuarios autenticados 

    def create_user(self):
        '''
        Crea un usuario para los @login_required
        '''
        password = 'userpass'
        user = User.objects.create_user(
            'user', 'user@test.com', password
        )
        return user, password

    def test_favorite(self):
        '''
        Comprueba el correcto funcionamiento para agregar una serie a favoritas
        '''
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post('/serie/twin-peaks/favorite/', 
            {'favorite': 'yes'},
            # AJAX!!
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        serie = m.Serie.objects.get(slug_name='twin-peaks')
        try:
            serie.favorite_of.get(user=user.profile)
            result = True
        except:
            result = False
        self.assertEqual(result, True)

    def test_form_add_serie(self):
        '''
        Comprueba el agregar una serie
        '''
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post('/series/add/', {
            'description_en': [u'Some description'],
            'description_es': [u'Alguna description'],
            'finished': [u'on'],
            'genres': ['1', '2'],
            'name_en': [u'Testing Add Serie EN'],
            'name_es': [u'Testing Add Serie ES'],
            'network': ['1'],
            'runtime': [u'30'],
        })
        # Nos va a redireccionar a la ficha de la serie, asi que es un 302
        self.assertEqual(response.status_code, 302)
        serie = m.Serie.objects.get(pk=2)
        self.assertEqual(serie.slug_name, 'testing-add-serie-en')

    def test_form_add_season(self):
        'Form de agregar temporada'
        season_number = 3
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post('/serie/twin-peaks/add/', {
            'season': season_number
        })
        message_ok = '{"redirect": "/serie/twin-peaks/", "message": "OK"}'
        self.assertEqual(response._get_content(), message_ok)
        self.assertEqual(response.status_code, 200)
        serie = m.Serie.objects.get(pk=1)
        season = m.Season.objects.get(serie=serie, season=season_number)
        self.assertEqual(season.season, season_number)


    def test_form_add_episode(self):
        '''
        Fform de agregar episodio
        '''
        url = '/series/lookup/serie/1/season/1/add/episode/'
        params = {
            'air_date': '01/01/2001',
            'title_es': 'Testing ES',
            'title_en': 'Testing EN',
            'title' : 'Testing EN',
            'episode': '9',
        }
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post(url, params)
        self.assertEqual(response.status_code, 200)
        message_ok = '"OK"'
        self.assertEqual(response._get_content(), message_ok)
        # Comprueba que efectivamente se agrego
        serie = m.Serie.objects.get(pk=1)
        season = m.Season.objects.get(serie=serie, season=1)
        episode = m.Episode.objects.get(season=season, episode=9)
        self.assertEqual(episode.episode, 9)

    def test_form_add_link(self):
        '''
        Form de agregar link
        '''
        url = '/series/links/add/episode/100/'
        url_check = 'http://www.megavideo.com/?d=FABADA'
        params = {
            'audio_lang' : '1',
            'subtitle' : '',
            'url' : url_check,
        }
        user, password = self.create_user()
        # Creamos USER_FOR_DEFAULT_LINKS
        password = 'userpass'
        user = User.objects.create_user(
            'liberateca', 'user@test.com', password
        )
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post(url, params)
        # Comrpueba que efectivamente se agrego
        self.assertEqual(response.status_code, 200)
        link = m.Link.objects.get(url=url_check)
        self.assertEqual(link.url, url_check)

    def test_vote_link(self):
        '''
        Votar por links
        '''
        url = '/series/links/vote/episode/'
        linkid = '83'
        params = {
            'linkid' : linkid,
            'vote' : 'upvote',
        }
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post(url, params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # Comprueba que efectivamente se agrego
        self.assertEqual(response.status_code, 200)
        message_ok = '{"score": 1, "num_votes": 1}'
        self.assertEqual(response._get_content(), message_ok)
        link = m.Link.objects.get(id=linkid)
        votes = Vote.objects.get_score(link)['score']
        self.assertEqual(votes, 1)

    def test_tracking_episodes(self):
        '''
        Seguimiento de series/episodios
        '''
        url = '/series/tracking/'
        serie_id = 1
        episode = 3
        season = 2
        params = {
            'serie_id': serie_id,
            'episode': episode,
            'season': season,
        }
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response = c.post(url, params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # Comprueba que efectivamente se agrego
        self.assertEqual(response.status_code, 200)
        message_ok = '"OK"'
        self.assertEqual(response._get_content(), message_ok)
        serie = m.Serie.objects.get(id=serie_id)
        season = m.Season.objects.get(serie=serie, season=season)
        episode = m.Episode.objects.get(season=season, episode=episode)
        # Esto ha de hacerse haciendo un filter contra el usuario, pero al 
        # ser un test con un unico usuario, da igual
        result = episode.viewed_episodes.exists()
        self.assertEqual(result, True)
        # Y el siguiente esta como no visto?
        result = episode.get_next_episode().viewed_episodes.exists()
        self.assertEqual(result, False)

    # Templatetags
    def test_background_color(self):
        ''' Prueba el templatetag de background color '''
        result = background_color(5)
        self.assertEqual(result, 'positive_bg')
        result = background_color(3)
        self.assertEqual(result, 'neutral_bg')
        result = background_color(1)
        self.assertEqual(result, 'negative_bg')
        result = background_color(0)
        self.assertEqual(result, 'no_bg')

    def test_echo_language(self):
        ''' Templatetag que devuelve el lenguaje '''
        result = echo_language('es')
        self.assertEqual(result, 'Español')
        result = echo_language('en')
        self.assertEqual(result, 'Inglés')
        result = echo_language('eu')
        self.assertEqual(result, 'Euskera')
        result = echo_language('ca')
        self.assertEqual(result, 'Catalán')
        result = echo_language('jp')
        self.assertEqual(result, 'Japonés')
        result = echo_language('xx')
        self.assertEqual(result, 'Desconocido')

    def test_extract_domain(self):
        ''' Templatetag que devuelve el dominio de una URL '''
        result = extract_domain('http://www.megavideo.com/?d=FABADA')
        self.assertEqual(result, 'megavideo.com')

    def test_extract_type(self):
        ''' Templatetag que devuelve el tipo de una URL '''
        result = extract_type('http://www.megavideo.com/?d=FABADA')
        self.assertEqual(result, 'Visionado online')
        result = extract_type('http://www.megaupload.com/?d=FABADA')
        self.assertEqual(result, 'Descarga directa')
        result = extract_type('http://www.mininova.org/?d=FABADA')
        self.assertEqual(result, 'Torrent')
        result = extract_type('http://www.xxxxxxx.org/?d=FABADA')
        self.assertEqual(result, 'Desconocido')

    def test_tagcloud(self):
        ''' Templatetag que devuelve el tagcloud para Genre/Network '''
        result = tagcloud('Genre', '1', '5')['tagcloud_list'][0]['name']
        self.assertEqual(result, 'Drama')
        result = tagcloud('Network', '1', '5')['tagcloud_list'][0]['name']
        self.assertEqual(result, 'ABC')

    # custom methods
    def test_next_season(self):
        ''' Comprueba get_next_season ''' 
        serie = m.Serie.objects.get(id=1)
        season = m.Season.objects.get(season=1, serie=serie)
        self.assertEqual(season.get_next_season().season, 2)

    def test_previous_season(self):
        ''' Comprueba get_previous_season ''' 
        serie = m.Serie.objects.get(id=1)
        season = m.Season.objects.get(season=2, serie=serie)
        self.assertEqual(season.get_previous_season().season, 1)
