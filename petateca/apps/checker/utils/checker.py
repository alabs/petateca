import re
from urllib2 import Request, urlopen
from urlparse import urlparse
from apps.checker.utils.checker_torrent import CheckerTorrent
from time import sleep

import logging

logger = logging.getLogger(__name__)

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

    def get_code(self, full_url):
        ''' Recibe URL y genera un diccionario con el dominio, la url y en el 
        caso  de Megavideo/Megaupload extrae el codigo (8 digitos) '''
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
        return code

    def get_status(self, url):
        ''' Recibe el codigo de Megavideo y devuelve si es buena o mala '''
        if url.startswith('http://www.megavideo.com/'):
            code = self.get_code(url)
            try:
                req = Request( "http://www.megavideo.com/xml/videolink.php?v=" + code['url_id'] )
            except TypeError:
                print code['full_url']
                return False
            page = urlopen(req); response=page.read(); page.close()
            errort = re.compile(' errortext="(.+?)"').findall(response)
            if len(errort) == 0:
                # No hay errores, el link es bueno
                return 'OK'
            else:
                return 'KO'
        elif url.startswith('http://www.megaupload.com/'):
            code = self.get_code(url)
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
        elif url.startswith('http://www.fileflyer.com/'):
            req = Request( url )
            page = urlopen(req); response=page.read(); page.close()
            if response.find('locked') != -1:
            # Archivo protegido (Locked) - requiere un codigo. No te queremos
                return "KO"
            elif response.find('fileslist') != -1:
            # Encontramos el listado de ficheros?
                return "OK"
            else:
                return "KO"
        elif url.startswith('http://www.fileserver.com/'):
            req = Request( url )
            page = urlopen(req); response=page.read(); page.close()
            if response.find('down_arrow') != -1:
            # Archivo para descargar (flecha verde)
                return "OK"
            else:
                return "KO"
        elif url.startswith('http://www.gigasize.com/'):
            req = Request( url )
            page = urlopen(req); response=page.read(); page.close()
            if response.find('Downloading') != -1:
            # Archivo para descargar (Downloading)
                return "OK"
            else:
                return "KO"
        elif url.startswith('http://www.mininova.org/'):
            # http://torrentfreak.com/mininova-filters-copyright-infringing-content-090506/  :(
            return 'KO'
        elif url.startswith('http://public.zoink.it/'):
            return CheckerTorrent(url).get_status() 
        elif url.startswith('http://torrent.zoink.it/'):
            return CheckerTorrent(url).get_status() 
        elif url.startswith('http://zoink.it/'):
            return CheckerTorrent(url).get_status() 
        elif url.startswith('http://www.bt-chat.com/'):
            # Tienen activado el throttle en bt-chat, asi que comprobamos que no nos 
            # hayan bloqueado, si nos bloquearon esperamos unos segundos y reintentamos
            response = urlopen(url).read()
            if response.find('Throttled') == -1: 
                return CheckerTorrent(url).get_status() 
            else:
                sleep(20) 
                return CheckerTorrent(url).get_status() 
        else:
            logger.error("LINK: Domain not valid - %s " % url)
            return False
