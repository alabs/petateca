#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
sys.path.append(".")
from liberbot.items import LiberBotItems

from scrapy import log
from scrapy.conf import settings
from scrapy.contrib.spiders import XMLFeedSpider

class EZRSSSpider(XMLFeedSpider):
    '''
    EZRSS: eztv.it RSS crawler, returns Items 'serie', 'titulo', 'temporada',
    'episodio', 'idioma', 'subtitulos', 'links' and 'sublink'. 

    Usage: python scrapy-ctl crawl ezrss 
    '''
    name = "ezrss"
    allowed_domains = ["ezrss.it"]

    start_urls = ['http://ezrss.it/feed/']
    iterator = 'iternodes' # This is actually unnecesary, since it's the default value
    itertag = 'item'
   # settings.overrides['EXPORT_FILE'] = 'sites/' + origname + '/dump/xmltest.p'

    def parse_node(self, response, node):
       # log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))
        item = LiberBotItems()
#        item['season'] = node.select('@Season').extract()
        title = node.select('title').extract()
        link = node.select('link').extract()
        category= node.select('category').extract()
        pubDate = node.select('category').extract()
        description = node.select('description')
        enclosure = node.select('enclosure').extract()
        comments = node.select('link').extract()
        guid = node.select('guid').extract()
        #print title, link, category, pubDate, description, enclosure, comments, guid
        
        yield item

SPIDER = EZRSSSpider()
