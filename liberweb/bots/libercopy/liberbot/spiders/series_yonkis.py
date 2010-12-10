# -*- coding: utf-8 -*-

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

import sys
sys.path.append(".")
from liberclass.askletter import AskLetter
from liberclass.fileextract import FileExtract
import Yonkis
from liberbot.items import LiberBotItems

class SeriesYonkisSpider(BaseSpider):
    '''
    seriesyonkis.com crawler, returns Items 'serie', 'title', 'temp',
    'epi', 'lang', 'sublang', 'links' and 'sublink'. 
    '''

    name = "series-yonkis"
    allowed_domains = ["seriesyonkis.com"]
 #   start_urls = ['http://www.seriesyonkis.com/serie/aeon-flux']

    letter = settings['LETTER']
    folder = settings['FOLDER']

    if letter and folder:
        import_file, export_file = AskLetter(letter,folder)
        settings.overrides['EXPORT_FILE'] = export_file
        start_urls = FileExtract(import_file)
    else:
        log.msg("Usage: scrapy crawl " + name + " --set LETTER=X --set FOLDER=X", level=log.INFO)

    def parse(self, response):
        '''
        Search for 'serie', 'title', 'temp', etc; all in the same page, for all the temp
        '''
        hxs = HtmlXPathSelector(response)

        episodes = hxs.select('//div[@id="tempycaps"]/ul/ul/li[@class="page_item"]/h5/a/@href')

        for episode in episodes:
            yield Request(episode.extract(), callback=self.parse_episode)

    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        '''
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()
        # Format: Serie - TempxEpi - Title
        #         Big Bang Theory - 3x23 - La excitacio³n lunar
        serie['serie'] = hxs.select('//div[@class="post"]/div/center/h2/a/text()').extract()[0]
        ntemp, nepi = hxs.select('//div[@class="post"]/div/h1/a/text()').re(r'(.*)x(.*) -')
        serie['temp'] = ntemp.decode('utf-8')
        serie['epi'] = nepi.decode('utf-8')

        lines = hxs.select('//div[@class="post"]/div/table/tr')

        for line in lines:
            # We get all tds, so if the line starts with 
            # Bandera - Idioma - Informador
            # we skep it 
            if line.select('.//span/text()')[0].extract() != u'Bandera':
                lang = line.select('.//img/@title')[0].extract()
                # If its a download, we capture the language from the 2nd image
                if lang == 'Descargar':
                    lang = line.select('.//img/@title')[1].extract()

                # Translate Languages/Subs
                if lang == u'Audio Español':
                    serie['lang'] = "es-es"
                elif lang == u'Audio Latino':
                    serie['lang'] = "es"
                elif lang == u'Subtítulos en Español':
                    serie['lang'] = "en"
                    serie['sublang'] = "es-es"
                elif lang == u'Audio Inglés':
                    serie['lang'] = "en"
                elif lang == u'Audio Catalan':
                    serie['lang'] = "ca"
                elif lang == u'Audio Euskera':
                    serie['lang'] = "eu"
                elif lang == u'Subtítulos en Inglés':
                    serie['lang'] = "en"
                    serie['sublang'] = "en"
                else:
                    print "LANGUAGE NOT FOUND!!!!"
                    print line.select('.//img/@title').extract()
    
                # Split and start fucking the link encrypted
                link_fuck = line.select('.//a/@href').extract()
                link_sep = link_fuck[0].split('=')
                
                # If using pymeno5, we crawl and decrypt
                if link_sep[0] == 'http://www.seriesyonkis.com/player/visor_pymeno5.php?d':
                    id = link_sep[-1]
                    ref = Yonkis.DecryptYonkis()
                    id_decrypted = ref.decryptID_series(ref.unescape(id))
                    link = 'http://www.megavideo.com/?v=' + id_decrypted
                else:
                # Also for downloads (descargar)
                    link_sep = link_fuck[0].split('/descargar/')
                    if link_sep[0] == 'http://www.seriesyonkis.com/lista-series':
                        id = link_sep[-1].split('/')[1]
                        ref = Yonkis.DecryptYonkis()
                        id_decrypted = ref.ccM(ref.unescape(id))
                        link = 'http://www.megaupload.com/?d=' + id_decrypted
                serie['links'] = link

                yield serie

SPIDER = SeriesYonkisSpider()
