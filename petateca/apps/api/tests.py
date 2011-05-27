"""
Tests para la API
"""

from django.test import TestCase
from django.contrib.auth.models import User

from simplejson import loads
import base64

class BaseAuthenticatedClient(TestCase):
    '''
    Autentica a los clientes usando auth basic. Basado en:
    http://thomas.pelletier.im/2009/12/test-your-django-piston-api-with-auth/
    '''
    def setUp(self):
        password = 'userpass'
        user = User.objects.create_user(
            'user', 'user@test.com', password
        )
        auth = '%s:%s' % (user.username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }


class APIAccessDenied(TestCase):

    def test_auth_required(self):
        "Comprueba que nos pide autenticacion para acceder a la API"
        url = '/api/v1/series/'
        r = self.client.get(url, {})
        self.assertEqual(r.status_code, 401)

class TestAPIAuth(BaseAuthenticatedClient):
    fixtures = ['test_data.json']

    def test_get_series_list(self):
        '''
        Listado de series
        '''
        url = '/api/v1/series/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        serie_name = loads(response._get_content())[0]['name']
        self.assertEqual(serie_name, 'Twin Peaks')

    def test_get_serie(self):
        '''
        Obtener una serie
        '''
        url = '/api/v1/series/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        serie_name = loads(response._get_content())['name']
        self.assertEqual(serie_name, 'Twin Peaks')

    def test_get_seasons(self):
        '''
        Obtener listado de temporadas de serie
        '''
        url = '/api/v1/series/1/seasons/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        season = loads(response._get_content())[0]['id']
        self.assertEqual(season, 1)

    def test_get_season(self):
        '''
        Obtener temporada de una serie dada
        '''
        url = '/api/v1/series/1/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        epi_title = loads(response._get_content())[0]['title']
        self.assertEqual(epi_title, 'Pilot')

    def test_get_episode(self):
        '''
        Obtener episodio y links de una serie/temporada/episodio
        '''
        url = '/api/v1/series/1/1/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        epi_link = loads(response._get_content())['links'][0]['url']
        self.assertEqual(epi_link, 'http://www.megavideo.com/?v=E001L7IE')
