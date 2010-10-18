# Scrapy settings for liberbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

# Bot Info
BOT_NAME = 'liberbot'
BOT_VERSION = '1.0'
USER_AGENT = 'LiberCopyBot - bots@libercopy.net'

# Scrapy stuff
SPIDER_MODULES = ['liberbot.spiders']
NEWSPIDER_MODULE = 'liberbot.spiders'
DEFAULT_ITEM_CLASS = 'liberbot.items.LiberBotItems'

# How many requests for spiders simultanously 
CONCURRENT_REQUESTS_PER_SPIDER = 2 #Default 8
DOWNLOAD_DELAY = 0.25    # 250 ms of delay. Default 0.

# Encoding
DEFAULT_RESPONSE_ENCODING='utf8'

# Cache
HTTPCACHE_DIR = 'liberbot/cache'
HTTPCACHE_EXPIRATION_SECS = '259200' # 72 horas
