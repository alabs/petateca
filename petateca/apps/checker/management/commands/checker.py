'''
    Busca los links y los procesa (deshabilitar o darle un +1)
'''

import re
from urllib2 import Request, urlopen
from urlparse import urlparse
import logging
from time import strftime, time
from datetime import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from serie import models as m

from voting.models import Vote


user = User.objects.get(username = settings.DEFAULT_USER_FOR_LINKS)
link_ct = ContentType.objects.get(app_label="serie", model="link")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '[actions ...]'
    help = '''
    Check and process the given links. 
    If the link is valid, it gets a +1 in voting. 
    If the link is invalid, it gets deactivated (not listed while listing links)

    Possible actions are 'all' and 'downvoted'. Example of use: 

    $ ./manage.py checker all
    $ ./manage.py checker downvoted
    '''

    def handle(self, *args, **options):
        if 'all' in args:
            process = ProcessLinks()
            process.process_all_links()
        elif 'downvoted' in args:
            process = ProcessLinks()
            process.process_downvoted()
        else:
            raise CommandError('%s is not a valid option' % (args[0]))


class Checker(object):
    '''
    Comprueba si un link es valido o no

    link = Checker(222)   # valor de link.id
    link.process()        # Encargado de procesar el link
    '''

    def get_id(self, type_d, url):
        '''
        Limpiamos los parametros GET de la URL

        Ejemplo: 
        *
        * 

        type_d dependera si se trata de megavideo o de maegaupload.
        Si es de megavideo, es ?v=
        Si es de megaupload, es ?d=
        '''
        query = urlparse(url).query.split('&')
        for q in query:
            q_splited = q.split('=')
            if q_splited[0] == type_d: return q_splited[1]
        return False

    def get_mega_code(self, full_url):
        ''' Recibe URL de Megavideo/Megaupload y extrae el codigo (8 digitos) '''
        if full_url.startswith('http://www.megavideo.com/'):
            code = {
                'domain': 'megavideo',
                'full_url': full_url,
                'url_id': self.get_id('v', full_url),
            }
        elif full_url.startswith('http://www.megaupload.com/'):
            code = {
                'domain': 'megaupload',
                'full_url': full_url,
                'url_id': self.get_id('d', full_url),
            }
        else:
            code = {
                'domain': 'notvalid',
                'full_url': full_url,
            }
            # fallback
        return code

    def get_status(self, url):
        ''' Recibe el codigo de Megavideo y devuelve si es buena o mala '''
        code = self.get_mega_code(url)
        if code['domain'] == 'megavideo':
            try:
                req = Request( "http://www.megavideo.com/xml/videolink.php?v=" + code['url_id'] )
            except TypeError:
                logger.error("Error al conseguir el codigo %s" % (code['url_id']) )
                return False
            page = urlopen(req); response=page.read(); page.close()
            errort = re.compile(' errortext="(.+?)"').findall(response)
            if len(errort) == 0:
                # No hay errores, el link es bueno
                return 'OK'
            else:
                return 'KO'
        elif code['domain'] == 'megaupload':
            # Pasamos las cabeceras para que no nos joda megavideo
            req = Request("http://www.megaupload.com/?d=" + code['url_id'])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            try:
                response = urlopen(req)
            except:
                req = Request(url.replace(" ","%20"))
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urlopen(req)
            data=response.read()
            response.close()
            patronvideos  = '<div.*?id="downloadlink"><a href="([^"]+)"'
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            if len(matches) > 0:
                # Se encontraron los enlaces, es bueno
                return 'OK'
            else:
                return 'KO'
        elif code['domain'] == 'notvalid':
            logger.error("LINK: Domain not valid - %s " % (code['full_url']))
            return False


class ProcessLinks(object):
    
    def link_upvote(self, link):
        '''
        Try to upvote the received link
        '''
        try: 
            is_upvoted = Vote.objects.get(content_type = link_ct, object_id=link.id, user=user).is_upvote()
            if is_upvoted:
                logger.info('LINK: %s - %s | STATUS: already upvoted' % (link.id, link.url))
        except Vote.DoesNotExist:
            Vote.objects.record_vote(link, user, +1)
            logger.info('LINK: %s - %s | STATUS: upvoted' % (link.id, link.url))
        return True

    def link_inactivate(self, link):
        '''
        Change the boolean property is_active of the received link
        '''
        if link.is_active:
            link.is_active = False
            link.save()
            logger.info('LINK: %s - %s | STATUS: inactive' % (link.id, link.url))
        else: 
            logger.info('LINK: %s - %s | STATUS: already inactive' % (link.id, link.url))
        return True

    def process(self, link): 
        ''' 
        Recibe un link y teniendo en cuenta el OK o el KO de resultado de la URL,
        procede a deshabilitarla o a darle un +1 en las votaciones
        '''
        try: 
            link = m.Link.objects.get(id=link.id)
        except m.Link.DoesNotExist:
            logger.error('Link does not exist')
            return False
        checker = Checker()
        result = checker.get_status(link.url)
        link.check_date = datetime.now()
        link.save()
        if result == 'KO':
            self.link_inactivate(link)
        elif result == 'OK': 
            self.link_upvote(link)

    def timer_start(self):
        '''
        Loggea y devuelve el tiempo de inicio en EPOCH.
        '''
        t_start = strftime("%a, %d %b %Y %H:%M:%S")
        i_start = time()
        logger.info('PROCESS LINKS - START CHECKING DOWNVOTED - %s' % (t_start))
        return i_start

    def timer_end(self, i_start):
        '''
        Loggea y hace el calculo de inicio a fin en segundos.
        Tiene que recibir la hora de inicio en EPOCH.
        '''
        t_end = strftime("%a, %d %b %Y %H:%M:%S")
        i_end = time()
        segundos_raw = i_end - i_start
        segundos = int(str(segundos_raw).split('.')[0])
        if segundos < 60: 
            elapsed = '%s segundos' % (segundos)
        else: 
            minutos = segundos / 60
            elapsed = '%s minutos' % (minutos)
        logger.info('PROCESS LINKS - FINISHED CHECKING DOWNVOTED - %s' % (t_end))
        logger.info('ELAPSED TIME: %s' % (elapsed))
        return True

    def process_downvoted(self):
        '''
        Process the downvoted links
        '''
        downvotes = Vote.objects.all()
        i_start = self.timer_start()
        for vote in downvotes:
            l = m.Link.objects.get(id=vote.object_id)
            self.process(l)
        self.timer_end(i_start)

    def process_all_links(self):
        '''
        Process all the links
        '''
        i_start = self.timer_start()
        for l in m.Link.objects.all(): 
            self.process(l)
        self.timer_end(i_start)


