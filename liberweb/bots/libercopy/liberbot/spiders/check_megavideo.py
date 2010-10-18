from scrapy.conf import settings
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider

class MegavideoSpider(CrawlSpider):
    name = 'check-megavideo'
    domain_name = 'megavideo.com'

    query = settings['QUERY']
    if query:
        start_urls = ['http://www.megavideo.com/?v=' + query]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        available = hxs.select('.//div[@id="mainpage"]/div/table/tr/td/span/text()').extract()
        if available == [u'This video is unavailable.']:
           print 'DIEE'

SPIDER = MegavideoSpider()

