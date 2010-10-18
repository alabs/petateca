# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LiberBotItems(Item):
    serie = Field()
    epi = Field()
    temp = Field()
    lang = Field()
    title = Field()
    links = Field()
    sublang = Field()
    sublink = Field()
    type = Field()
    pass

