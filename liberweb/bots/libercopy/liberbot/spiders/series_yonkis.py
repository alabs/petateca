#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

import sys
sys.path.append(".")
from liberclass.askletter import AskLetter
from liberclass.fileextract import FileExtract
#from liberclass.crawlerjs import CrawlerJS
from liberbot.items import LiberBotItems

class SeriesYonkisSpider(BaseSpider):
    '''
    seriesyonkis.com crawler, returns Items 'serie', 'title', 'temp',
    'epi', 'lang', 'sublang', 'links' and 'sublink'. 
    '''

    name = "series-yonkis"
    allowed_domains = ["seriesyonkis.com"]
    start_urls = ['http://www.seriesyonkis.com/serie/alf']

   # letter = settings['LETTER']
   # folder = settings['FOLDER']

   # if letter and folder:
   #     import_file, export_file = AskLetter(letter,folder)
   #     settings.overrides['EXPORT_FILE'] = export_file
   #     start_urls = ['http://www.seriesyonkis.com/serie/alf'] #FileExtract(import_file)
   # else:
   #     log.msg("Usage: scrapy crawl " + name + " --set LETTER=X --set FOLDER=X", level=log.INFO)

    def parse(self, response):
        '''
        Search for 'serie', 'title', 'temp', etc; all in the same page, for all the temp
        '''
        hxs = HtmlXPathSelector(response)

        episodes = hxs.select('//div[@id="tempycaps"]/ul/ul/li[@class="page_item"]/h5/a/@href').extract()

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
        serie['serie'] = hxs.select('//div[@class="post"]/div/center/h2/a/text()').extract()
        serie['temp'], serie['epi'] = hxs.select('//div[@class="post"]/div/h1/a/text()').re(r'(.*)x(.*) -')

        serie['type'] = "VerOnline"

        veronline = hxs.select('//div[@class="post"]/div/table/tr')

        for line in enumerate(veronline):
            lang = veronline[line]('.//div/span/text()')[2].extract()
            subtitle = veronline[line]('.//div/span/text()')[3].extract()

            if lang == [u'Dual']:
                serie['lang'] = "Dual"
            elif lang == [u'V.O']:
                serie['lang'] = "English"
            elif lang == [u'Espa\xf1ol']:
                serie['lang'] = "Spanish"
            elif lang == [u'V.O.S.E']:
                serie['lang'] = "English"
                serie['sublang'] = "Spanish"

            link = veronline[line]('.//a/@href').extract()

            # SeriesYonkis checks trough JS if you're a real client... We see an error page :S
            request = CrawlerJS('link').crawl()
            hxs = HtmlXPathSelector(request)
            
            yield serie

SPIDER = SeriesYonkisSpider()
