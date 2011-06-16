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
        url = '/api/v2/series/'
        r = self.client.get(url, {})
        self.assertEqual(r.status_code, 401)

class TestAPIAuth(BaseAuthenticatedClient):
    fixtures = ['twin_peaks.json']

    def json_response(self, response):
        return loads(response._get_content())

    def test_get_series_list(self):
        '''
        Listado de series
        '''
        url = '/api/v2/series/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        serie_name = self.json_response(response)[0]['name_es']
        self.assertEqual(serie_name, 'Twin Peaks')

    # TODO: comprobar pagination

    def test_get_serie(self):
        '''
        Obtener una serie
        '''
        url = '/api/v2/series/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        json_response = loads(response._get_content())
        serie_name = json_response['name_es']
        self.assertEqual(serie_name, 'Twin Peaks')
        thumbnail = json_response['poster']['thumbnail']
        img = 'http://example.com/static/cache/6d/11/6d11de6c41317323c8fe535322fab6ee.jpg'
        self.assertEqual(img, thumbnail)

    def test_get_seasons(self):
        '''
        Obtener listado de temporadas de serie
        '''
        url = '/api/v2/series/1/seasons/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        season = self.json_response(response)[0]['id']
        self.assertEqual(season, 1)

    def test_get_season(self):
        '''
        Obtener temporada de una serie dada
        '''
        url = '/api/v2/series/1/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        epi_title = self.json_response(response)[0]['title']
        self.assertEqual(epi_title, 'Pilot')

    def test_get_episode(self):
        '''
        Obtener episodio y links de una serie/temporada/episodio
        '''
        url = '/api/v2/series/1/1/1/'
        response = self.client.get(url, {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        epi_link = self.json_response(response)['links'][0]['url']
        self.assertEqual(epi_link, 'http://www.megavideo.com/?v=E001L7IE')
