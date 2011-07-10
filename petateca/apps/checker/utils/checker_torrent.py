from core.lib import bencode
from urllib import urlencode
from hashlib import sha1
from urllib2 import urlopen, URLError

class CheckerTorrent(object):
    ''' Comprobador de ficheros torrents '''

    def __init__(self, file_torrent):
        self.file_torrent = file_torrent

    def info_hash(self, info_torrent):
        ''' Transforma el valor info en el infohash '''
        info = info_torrent['info']
        return sha1(bencode.encode(info)).hexdigest()

    def return_info(self, file_torrent):
        if file_torrent.startswith('http://'):
            info_torrent = bencode.decode(urlopen(file_torrent).read())
        else:
            info_torrent = bencode.decode(open(file_torrent).read()) 
        return info_torrent

    def scrape_trackers(self, info, info_torrent):
        query = urlencode( [('info_hash', info)] )
        complete, downloaded, incomplete = [], [], []
        for tracker in info_torrent['announce-list']:
            scrape_url = tracker[0].replace('announce', 'scrape')
            url = scrape_url + '?' + query
            try: 
                response = urlopen(url, timeout=5).read()
                resp = bencode.decode(response)
                torrent_scraped = resp['files'][resp['files'].keys()[0]]
                complete.append(torrent_scraped['complete'])
                downloaded.append(torrent_scraped['downloaded'])
                incomplete.append(torrent_scraped['incomplete'])
            except URLError:
                pass
        complete.sort()
        downloaded.sort()
        incomplete.sort()
        return {
            'complete' :  complete[-1],
            'downloaded': downloaded[-1],
            'incomplete': incomplete[1]
        }

    def scrape_torrent(self):
        ''' 
        Recibe un fichero o una URL con un torrent y devuelve la cantidad
        maxima de completos, descargados e incompletos que se consiguen de 
        los trackers comprobandolo en /scrape
        '''
        info_torrent = self.return_info(self.file_torrent)
        info_hash = self.info_hash(info_torrent).decode('hex')
        return self.scrape_trackers(info_hash, info_torrent)
