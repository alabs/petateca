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
from string import strip

class SeriesDankoSpider(BaseSpider):
    '''
    seriesdanko.com crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = 'series-danko'
    allowed_domains = ['seriesdanko.com']
 
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
        epis = hxs.select('//div[@class="post-body entry-content"]/a/@href')
        for episode in epis:
            yield Request(episode.extract(), callback=self.parse_episode)

    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        '''
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()
        # Format: Serie - TempxEpi - Title
        #         Dexter 1x01 Capitulo 01 
        serie['serie'], serie['temp'], serie['epi'] = hxs.select('//h3[@class="post-title entry-title"]/a/text()').re(r'(.*) (\d*)x(\d*)')
        
        serie['serie'] = serie['serie'][0].encode('utf-8')
        serie['temp'] = serie['temp'][0].encode('utf-8')
        serie['epi'] = serie['epi'].encode('utf-8') 

        # Let's go to language and links, please... Exclude both the "Ver Capitulo X online" and "Idioma - Fecha - Servidor... "
        tableraw = hxs.select('//table/tbody/tr[not(td[@class="verde padlados"])][not(td[@class="tam13"])][not(td[@class="tam11"])]')

        for index, tipo in enumerate(tableraw):
            trraw = tableraw[index]

            def chooselang(img):
                ''' Returns lang based on img flag '''
                VOS = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbe1uWzX_I/AAAAAAAAAEM/NVlJkuICjag/s320/vos.png"
                esp = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbaaxbSUhI/AAAAAAAAADs/D2MlOyqWc74/s320/es.png"
                eng = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbe1EQZTbI/AAAAAAAAAEE/xkoq2JAsHA4/s320/vo.png"
                lat = "http://3.bp.blogspot.com/_92FLPSdwaw0/TAbet_dPNEI/AAAAAAAAAD8/tiwSbaXbSpI/s320/la.png"
                sublang = ''
                if img == VOS:
                    lang = "English"
                    sublang = "Spanish"
                elif img == esp:
                    lang = "Spanish"
                elif img == lat: 
                    lang = "Latin" 
                elif img == eng: 
                    lang = "English" 
                return lang, sublang
            
            # Ask lang and sublang
            img = trraw.select('.//img/@src')[0].extract().encode('utf-8')
            serie['lang'], serie['sublang'] = chooselang(img)
            # Cleans sublang
            if serie['sublang'] == '':
                del serie['sublang']

            # Ask for type:
            serie_type = trraw.select('.//a/text()').extract()
            if serie_type == [u'Ver']:
                serie['type'] = 'VerOnline'
            elif serie_type == [u'Descargar']:
                serie['type'] = 'Descargar'

            # Ask for links
            serie['links'] = trraw.select('.//a/@href')[0].extract().encode('utf-8')
            yield serie


Spider = SeriesDankoSpider()
