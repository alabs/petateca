from django.test import TestCase, Client
from django.contrib.auth.models import User

from serie import models as m

class TrackingTest(TestCase):
    fixtures = ['twin_peaks.json']

    def create_user(self):
        '''
        Crea un usuario para los @login_required
        '''
        password = 'userpass'
        user = User.objects.create_user(
            'user', 'user@test.com', password
        )
        return user, password

    def test_tracking_set(self):
        '''
        Seguimiento de series/episodios, seguir a un episodio
        '''
        url = '/tracking/set/'
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


    def test_tracking_show(self):
        '''
        Seguimiento de series/episodios, mostrar los episodios
        '''
        # Primero hacemos un set
        url_set = '/tracking/set/'
        serie_id_set = 1
        episode_set = 3
        season_set = 2
        params_set = {
            'serie_id': serie_id_set,
            'episode': episode_set,
            'season': season_set,
        }
        user, password = self.create_user()
        c = Client()
        c.login(username=user.username, password=password)
        response_set = c.post(url_set, params_set,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response_set.status_code, 200)

        # Ahora toca el show
        url = '/tracking/show/'
        serie_id = 1
        params = {
            'serie_id': serie_id,
        }
        response_show = c.post(url, params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response_show.status_code, 200)
        # Comprobamos que este devolviendo los episodios
        self.assertContains(response_show, '/series/links/list/1/2/8/')
