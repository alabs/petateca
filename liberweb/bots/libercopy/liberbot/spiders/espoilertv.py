#!/usr/bin/python 
# -*- coding: iso-8859-15 -*- 

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

import sys
sys.path.append(".")
from liberclass.askletter import AskLetterEspoilerTV
from liberbot.items import LiberBotItems

class EspoilerTVSpider( BaseSpider ):
    '''
    espoilertv.com crawler, returns Items 'serie', 'title', 'temp',
    'epi', 'lang', 'sublang', 'links' and 'sublink'. 
    '''

    name = 'espoilertv'
    allowed_domains = ['espoilertv.com']

    letter = settings['LETTER']
    folder = settings['FOLDER']

    if letter and folder:
        import_url, export_file = AskLetterEspoilerTV(letter,folder)
        start_urls = import_url
    else:
        log.msg("Usage: scrapy crawl " + name + " --set LETTER=X --set FOLDER=X", level=log.INFO)


    def parse(self, response):
        '''
        Search links of episodes in series, send it to parse_episode 
        '''
        hxs = HtmlXPathSelector(response)

        raw_series = hxs.select('.//html/body/div[@class="cont"]/div[@class="lista_series"]/div[@class="obj"]/div[@class="barra"]/h2/@onclick')
        raw_series.re(r'\((.*)\)')

        for serie in raw_series.re(r'\((.*)\)'):
            serie = serie.split(',')
            url_temp = 'http://espoilertv.com/ajax/temporada.php?idserie=' + serie[0] + '&temporada=' + serie[1]
            print url_temp

#Request(episode.extract(), callback=self.parse_episode)


#        # Looking for: http://www.tumejortv.com/series-tv-online/a-dos-metros-bajo-tierra/a-dos-metros-bajo-tierra-temporada-1/capitulo-112-24-11-04-2009.html
#        linklistados = hxs.select('//ul[@class="linksListados"]')
#
#        epis = []
#        for index, listado in enumerate(linklistados):
#            epis.append(linklistados[index].select('.//a/@href').extract())
#
#        for episode in epis:
#            yield Request(episode.extract(), callback=self.parse_episode)
#
#
#
#
