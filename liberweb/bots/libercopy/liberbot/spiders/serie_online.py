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

class SerieOnlineSpider(BaseSpider):
    '''
    serieonline.net crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = 'serie-online'
    allowed_domains = ['serieonline.net']

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
        for episode in hxs('//div[@class="serie"]/a/@href'):
            yield Request(episode.extract(), callback=self.parse_episode)

    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        ''' 
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()
        # Format: Serie - TempxEpi - Title
        #         Big Bang Theory - 3x23 - La excitacio³n lunar
        serie['serie'] = hxs.select('//div[@class="titulo"]/h3/text()').re(r'(.*) - \d*x*\d* - .*')
        serie['title'] = hxs.select('//div[@class="titulo"]/h3/text()').re(r'.* - \d*x*.*\d* - (.*)')
        serie['temp'] = hxs.select('//div[@class="titulo"]/h3/text()').re(r'.* - (\d*)x*\d* - .*')
        serie['epi'] = hxs.select('//div[@class="titulo"]/h3/text()').re(r'.* - .*x(\d*) - .*')
        serie['serie'] = serie['serie'][0].encode('utf-8')
        serie['title'] = serie['title'][0].encode('utf-8')
        serie['temp'] = serie['temp'][0].encode('utf-8')
        serie['epi'] = serie['epi'][0].encode('utf-8') 
        serie['type'] = "VerOnline" 

        # Let's go to language and links, please...
        for index, lang in enumerate(hxs.select('//p[contains(@class, "tabla")]')):
            tabla = hxs.select('//p[contains(@class, "tabla")]')[index]

            # Searching 'lang' - language -  and 'sublang' - subtitle language. 
            lang = tabla('.//strong/text()').extract()
            if lang == [u'Dual']:
                serie['lang'] = "English"
            elif lang == [u'V.O']:
                serie['lang'] = "English"
            elif lang == [u'Espa\xf1ol']:
                serie['lang'] = "Spanish"
            elif lang == [u'Dual Esp-Jap']:
                serie['lang'] = "Japanese"
            elif lang == [u'V.O.S.E']:
                serie['lang'] = "English"
                serie['sublang'] = "Spanish"

            # Search for "http://www.serieonline.net/subtitulos/series" 
            sublink = tabla('.//a[contains(@href,"http://www.serieonline.net/subtitulos/series")]/@href').extract()
            if sublink: 
                serie['sublink'] = sublink

            # Links opens in new window (<a target="blank">) 
            links = tabla('.//a[contains(@target, "_blank")]/@href').extract()

            for link in links:
                serie['links'] = link.encode('utf-8')
                yield serie
  
            try: 
                links = hxs.select('//input[@id="ver-megavideo"]/@onclick').re('.*\(\'(.*)\'')
                for link in links:
                    if not link == '':
                        serie['links'] = link.encode('utf-8')
            except: 
                pass

            try:
                links = hxs.select('//input[@id="ver-fileflyer"]/@onclick').re('.*\(\'(.*)\'')
                for link in links:
                    if not link == '':
                        serie['links'] = link.encode('utf-8')
                        yield serie
            except: 
                pass

SPIDER = SerieOnlineSpider()
