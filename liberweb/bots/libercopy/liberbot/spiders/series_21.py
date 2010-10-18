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

class Series21Spider(BaseSpider):
    '''
    series21.com crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = 'series-21'
    allowed_domains = ['series21.com']
 
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
        serietemp = hxs.select('//div[@class="serietemporadas"]')

        temps = []
        for index, temp in enumerate(serietemp):
            temps.append(serietemp[index].select('.//a/@href').extract())

        for temp in temps:
            for epi in temp:
                full_epi = 'http://www.series21.com' + epi
                yield Request(full_epi, callback=self.parse_episode)


    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        '''
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()

        serie['serie'] = hxs.select('//h1/a/text()')[0].extract()
        serie['temp'], serie['epi'], epi_title = hxs.select('//h1/text()').re(r' (\d)x(\d*) - (.*)')

        # Let's go to language and links, please...
        tableraw = hxs.select('//div[@class="lista marcar"]')

        for index, tipo in enumerate(tableraw):
            trraw = tableraw[index]
            serie['links'] = trraw.select('.//a/@href')[0].extract()
            try: 
                #  u'/images/esp.gif'
                trraw.select('.//img/@src')[0].extract()
                serie['lang'] = "Spanish"
            except:
                # u'Subtitulado'
                trraw.select('.//span[@class="bloque-doblaje"]/text()')[0].extract()
                serie['lang'] = "English"
                serie['sublang'] = "Spanish"
            finally:
                yield serie

Spider = Series21Spider()
