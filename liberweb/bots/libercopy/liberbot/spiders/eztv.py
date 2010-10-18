#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
sys.path.append(".")
from liberclass.askletter import AskLetter
from liberclass.fileextract import FileExtract
from liberbot.items import LiberBotItems

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from string import strip

class EZTVSpider(BaseSpider):
    '''
    eztv.it crawler, returns Items 'serie', 'title', 'temp',
    'epi', 'lang', 'sublang', 'links' and 'sublink'. 
    '''

    name = "eztv"
    allowed_domains = ["eztv.it"]

    letter = settings['LETTER']
    folder = settings['FOLDER']

    if letter and folder:
        import_file, export_file = AskLetter(letter,folder)
        start_urls = FileExtract(import_file)
    else:
        log.msg("Usage: scrapy crawl " + name + " --set LETTER=X --set FOLDER=X", level=log.INFO)

    def parse(self, response):
        '''
        Search for 'serie', 'title', 'temp', etc; all in the same page, for all the temp
        '''
        hxs = HtmlXPathSelector(response)

        # Search title
        title = hxs.select('//td[contains(@class,"section_post_header")]/b/text()')[0].extract()

        # Check if OFFLINE mode is on
        #try:
        #    # Search title
        #    title = hxs.select('//td[contains(@class,"section_post_header")]/b/text()')[0].extract()
        #except:
        #    offline = hxs.select('//html/body/div[@id="header_holder"]/center/b/text()').extract()
        #    if offline == [u'OFFLINE']:
        #        log.msg("EZTV is in OFFLINE mode", level=log.WARNING)
        #        sys.exit()

        # Bigtable: <table class="forum_header_noborder"> 
        bigtable = hxs.select('//table[contains(@class, "forum_header_noborder")]')

        # Every <tr> is an epi
        for index, link in enumerate(bigtable.select('.//tr[contains(@class, "forum_header_border")]')):
            # They dont have a standard, S[T]E[E] and [T]x[E]
            try: 
                season, episode = link.select('.//a[contains(@class, "epinfo")]/text()').re(r'S(\d*)E(\d*)')
            except:
                season, episode = link.select('.//a[contains(@class, "epinfo")]/text()').re(r'(\d*)x(\d*)')

            # Items, checkout en items.py
            serie = LiberBotItems()
            serie['serie'] = title.encode('UTF-8')
            serie['temp'] = season.encode('UTF-8')
            serie['epi'] = episode.encode('UTF-8')
            serie['lang'] = "English"
            serie['type'] = "Torrent"

            # torrents - TOR - and magnets - MAG - go to a list
            links = link.select('.//a[contains(@class, "download")]/@href')
            tor = []
            for index,link in enumerate(links): 
                tor.append(link.extract())
            MAG = link.select('.//a[contains(@class, "magnet")]/@href').extract()
            if MAG:
                tor.append(link.extract())
            
            for link in tor:
                serie['links'] = link.encode('utf-8')
                yield serie
            
