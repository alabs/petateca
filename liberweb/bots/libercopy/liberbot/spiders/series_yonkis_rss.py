#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from scrapy import log
from scrapy.conf import settings
from scrapy.contrib.spiders import XMLFeedSpider

import sys
sys.path.append(".")
from liberclass.askletter import AskRSSLetter
from liberbot.items import LiberBotItems

class SeriesYonkisRSSSpider(XMLFeedSpider):
    '''
    seriesyonkis.com RSS crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 
    '''

    name = "series-yonkis-rss"
    allowed_domains = ["feeds.feedburner.com"]
    iterator = 'iternodes'
    itertag = 'item'
    folder = settings['FOLDER']

    if folder:
        export_rss_file = AskRSSLetter(folder)
        settings.overrides['EXPORT_FILE'] = export_rss_file
        start_urls = ['http://feeds.feedburner.com/ultimoscapitulos?format=xml']
    else:
        log.msg("Usage: scrapy crawl " + name + " --set FOLDER=X", level=log.INFO)

    def parse_node(self, response, node):
        item = LiberBotItems()
        title = node.select('title').extract()
        link = node.select('link').extract()
        guid = node.select('guid').extract()
        pubDate = node.select('category').extract()
        description = node.select('description')
        feedburner = node.select('enclosure').extract()
        print title, link, guid, pubDate, description, feedburner

        # Return Items
        yield item

SPIDER = SeriesYonkisRSSSpider()
