#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
sys.path.append(".")
from liberclass.askletter import AskLetter
from liberclass.fileextract import FileExtract
from liberbot.items import LiberBotItems

from scrapy.conf import settings
from scrapy.http import Request 
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy import log

from urllib2 import urlopen
import re
            
class CineTubeSpider(BaseSpider):
    '''
    cinetube.es crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = 'cinetube'
    allowed_domains = ['cinetube.es']

    letter = settings['LETTER']
    folder = settings['FOLDER']

    if letter and folder:
        import_file, export_file = AskLetter(letter,folder)
        start_urls = FileExtract(import_file)
    else:
        log.msg("Usage: scrapy crawl " + name + " --set LETTER=X --set FOLDER=X", level=log.INFO)

    def parse(self, response):
        ''' 
        Search links of episodes in series, send it to parse_episode 
        ''' 
        hxs = HtmlXPathSelector(response)
        # Looking for: http://www.serieonline.net/big-bang-theory/temporada-3/23/
        for temp in hxs.select('//h2/a/@href'):
            yield Request('http://www.cinetube.es' + temp.extract(), callback=self.parse_temp)

    def parse_temp(self, response):
        '''
        Goes for every temp looking for every episode
        '''
        hxs = HtmlXPathSelector(response)
        epis = hxs.select('//div[@class="block"]/a/@href')

        for epi in epis:
            yield Request('http://www.cinetube.es' + epi.extract(), callback=self.parse_episode)

    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        ''' 
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()
        # Format: Serie >> Temporada X >> Capitulo X
        #         El diario de Daniela » Temporada 1 » Capitulo 11
        serie['serie'], n_temp, n_epi = hxs.select('//a[@class="link"]/text()').extract()
        serie['temp'] = n_temp.replace('Temporada ','')
        serie['epi'] = n_epi.replace('Capitulo ','')
        #serie['serie'] = serie['serie'].encode('utf-8')
        #serie['temp'] = serie['temp'].encode('utf-8')
        #serie['epi'] = serie['epi'].encode('utf-8') 

        links_raw = hxs.select('//div[@class="tit_opts"]')
        
        for link in links_raw:
            last_link = link.select('.//a/@href')[0]
            lang = link.select('.//span/text()').re(r'IDIOMA: (.*)')
            if lang == [u'LATINO']:
                serie['lang'] = "es"
            elif lang == [u'ESPA\xd1OL']:
                serie['lang'] = "es-es"
            elif lang == [u'SUB']:
                serie['lang'] = "en"
                serie['sublang'] = 'es-es'
            # Last redirection for getting the fucking link, really??
            last_link = 'http://www.cinetube.es' + last_link.extract()
            # We can't do another callback, scrapy forgets the serie element :S
            # So... 
            link = urlopen(last_link)
            html = link.read()
            # Yeaaaahhh Fucking Regexp to the rescue!!!
            try: 
                serie['links'] = re.search(r'<li id="(.*)"><a ', html).group(1) 
            except:
                serie['links'] = re.search(r'<h3><a href="(.*)" target', html).group(1)
            finally:
                yield serie

SPIDER = CineTubeSpider()
