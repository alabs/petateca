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

class SeriesPepitoSpider(BaseSpider):
    '''
    seriespepito.com crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = 'series-pepito'
    allowed_domains = ['seriespepito.com']

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
 
        # Looking for: http://www.series...
        for episode in hxs.select('//li[@class="li_capitulo"]/a/@href'):
            yield Request(episode.extract(), callback=self.parse_episode)

    def parse_episode(self, response):
        '''
        xpathselector to the rescue! Search for 'serie', 'titulo', 'temporada', etc
        '''
        hxs = HtmlXPathSelector(response)
        serie = LiberBotItems()
        # Formato: Serie - TemporadaxEpisodio - Titulo
        # Ejemplo: Big Bang Theory 3x23 - La excitacio³n lunar
        serie_name, serie['temp'], serie['epi'], serie['title'] = hxs.select('//span[@class="tam12"]/text()')[0].re(r'(.*) (.*)x(.*) - (.*)')
        serie['serie'] = serie_name.strip()
        serie['serie'] = serie['serie'].encode('utf-8')
        serie['title'] = serie['title'].encode('utf-8')
        serie['temp'] = serie['temp'].encode('utf-8')
        serie['epi'] = serie['epi'].encode('utf-8') 

        tablas = hxs.select('//table[@width="620"]')

        # Ahora viene lo dificil, ir verificando los idiomas que hay disponible y consiguiendo los links
        for index, lang in enumerate(tablas):
            tabla = tablas[index]

           # tabla.select('.//td[@class="tam12"]/text()').re(r'No hay registros disponibles .*')

            img = tabla.select('//img[@width="30"]/@src')[0].extract()
            ''' Returns lang based on img flag '''
            VOS = "http://www.seriespepito.com/seriespepito/idiomas/vos.png"
            esp = "http://www.seriespepito.com/seriespepito/idiomas/es.png"
            eng = "http://www.seriespepito.com/seriespepito/idiomas/vo.png"
            lat = "http://www.seriespepito.com/seriespepito/idiomas/la.png"
            if img == VOS:
                serie['lang'] = "English"
                serie['sublang'] = "Spanish"
            elif img == esp:
                serie['lang'] = "Spanish"
            elif img == lat: 
                serie['lang'] = "Latin" 
            elif img == eng: 
                serie['lang'] = "English" 

#            lang = tabla.select('.//strong/text()').extract()

            links = tabla('.//a[contains(@target, "_blank")]/@href').extract()

            for link in links:
                serie['links'] = link.encode('utf-8')
                subtitulos = tabla('.//a[contains(@href,"http://www.serieonline.net/subtitulos/series")]/@href').extract()
                if subtitulos:
                    serie['sublink'] = subtitulos
                yield serie

            # ARRRGHHH por la puta enie no puedo hacer esto que quedaria mas mejor:
            # subtitulos = tabla(".//a[text()=u'Descargar subt\xedtulos en Espa\xf1ol']/@href").extract()
            # Asi que le digo al xpath que el link sea de /subtitulos/series. Si, no es lo mas lindo, pero alguien tiene que hacerlo 
            #subtitulos = tabla('.//a[contains(@href,"http://www.serieonline.net/subtitulos/series")]/@href').extract()
            #if subtitulos: 
            #    serie['sublink'] = subtitulos
            #print serie

            ## Devolvemos los Items al pipeline ;) 
            #yield serie

SPIDER = SeriesPepitoSpider()
