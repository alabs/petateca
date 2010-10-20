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

class TuMejorTVSpider(BaseSpider):
    '''
    tumejortv.com crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''
     
    name = 'tumejortv'
    allowed_domains = ['tumejortv.com']

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
        # Looking for: http://www.tumejortv.com/series-tv-online/a-dos-metros-bajo-tierra/a-dos-metros-bajo-tierra-temporada-1/capitulo-112-24-11-04-2009.html
        linklistados = hxs.select('//ul[@class="linksListados"]')

        epis = []
        for index, listado in enumerate(linklistados):
            epis.append(linklistados[index].select('.//a/@href').extract())
        
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
        serie['serie'], serie['temp'], serie['epi'] = hxs.select('//h3/a/text()').re('.*, (.*) Temporada (.*), Capitulo (.*)')

#        # Let's go to language and links, please...
#        tableraw = hxs.select('//table/tbody/tr')
#
#        for index, tipo in enumerate(tableraw):
#            trraw = tableraw[index]
#
#            def chooselang(img):
#                ''' Returns lang based on img flag '''
#                VOS = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbe1uWzX_I/AAAAAAAAAEM/NVlJkuICjag/s320/vos.png"
#                esp = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbaaxbSUhI/AAAAAAAAADs/D2MlOyqWc74/s320/es.png"
#                eng = "http://2.bp.blogspot.com/_92FLPSdwaw0/TAbe1EQZTbI/AAAAAAAAAEE/xkoq2JAsHA4/s320/vo.png"
#                lat = "http://3.bp.blogspot.com/_92FLPSdwaw0/TAbet_dPNEI/AAAAAAAAAD8/tiwSbaXbSpI/s320/la.png"
#                if img == VOS:
#                    lang = "English"
#                    sublang = "Spanish"
#                elif img == esp:
#                    lang = "Spanish"
#                elif img == lat: 
#                    lang = "Latin" 
#                elif img == eng: 
#                    lang = "English" 
#                return lang, sublang
#            
#            type = trraw.select('.//a/text()').extract()
#            if type == [u'Ver'] or [u'Descargar']:
#                serie['type'] = type
#                serie['links'] = trraw('.//a/@href').extract()
#                return serie

Spider = TuMejorTVSpider()
