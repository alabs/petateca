from scrapy.conf import settings
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider

class MegauploadSpider(CrawlSpider):
    name = 'check-megaupload'
    domain_name = 'megaupload.com'

    query = settings['QUERY']
    if query:
        start_urls = ['http://www.megaupload.com/?d=' + query]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        megavideo_link = hxs.select('//div[@id="main"]/div/div/div/table/tr/td/table/tr/td/a/@href')[1].extract()

        available = hxs.select('//table/tr/td/text()')[0].extract()
        if available == [u'- Invalid link']:
           print 'DIEE'


SPIDER = MegauploadSpider()
