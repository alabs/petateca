#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from liberbot.items import LiberBotItems
from scrapy import log
from scrapy.conf import settings
from scrapy.contrib.spiders import XMLFeedSpider

class SerieOnlineRSSSpider(XMLFeedSpider):
    '''
    serieonline.net RSS crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 

    Usage: python scrapy-ctl crawl serie-online-rss 
    '''
    name = "serie-online-rss"
    allowed_domains = ["feeds.feedburner.com"]

    start_urls = ['http://feeds.feedburner.com//serieonline/series?format=xml']
    iterator = 'iternodes' # This is actually unnecesary, since it's the default value
    itertag = 'item'
   # settings.overrides['EXPORT_FILE'] = 'sites/' + origname + '/dump/xmltest.p'

    def parse_node(self, response, node):
       # log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))
        item = LiberBotItems()
#        item['season'] = node.select('@Season').extract()
        title = node.select('title').extract()
        link = node.select('link').extract()
        guid = node.select('guid').extract()
        pubDate = node.select('category').extract()
        description = node.select('description')
        feedburner = node.select('enclosure').extract()
        print title, link, guid, pubDate, description, feedburner

        # Return Items
        yield item

SPIDER = SerieOnlineRSSSpider()
