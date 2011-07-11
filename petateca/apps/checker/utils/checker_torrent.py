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
            try:
                info_torrent = bencode.decode(urlopen(file_torrent).read())
            except:
                import ipdb; ipdb.set_trace()
        else:
            info_torrent = bencode.decode(open(file_torrent).read()) 
        return info_torrent

    def scrape_trackers(self, info, info_torrent):
        query = urlencode( [('info_hash', info)] )
        complete, downloaded, incomplete = [], [], []
        try:
            announces = info_torrent['announce-list']
        except KeyError:
            announces = []
            announces.append(info_torrent['announce'])
        for tracker in announces:
            scrape_url = tracker.replace('announce', 'scrape')
            url = scrape_url + '?' + query
            try: 
                response = urlopen(url, timeout=5).read()
                resp = bencode.decode(response)
                try:
                    torrent_scraped = resp['files'][resp['files'].keys()[0]]
                    complete.append(torrent_scraped['complete'])
                    downloaded.append(torrent_scraped['downloaded'])
                    incomplete.append(torrent_scraped['incomplete'])
                except IndexError:
                    pass
            except URLError:
                pass
        complete.sort()
        downloaded.sort()
        incomplete.sort()
        if not complete: complete = [0]
        if not downloaded: downloaded = [0] 
        if not incomplete: incomplete = [0] 
        return {
            'complete' :  complete[-1],
            'downloaded': downloaded[-1],
            'incomplete': incomplete[-1]
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

    def get_status(self):
        result = self.scrape_torrent()
        if result['complete'] == 0:
            return 'KO'
        else: 
            return 'OK'
