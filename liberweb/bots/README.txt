Bienvenido a los Bots de LiberCopy!!

Antes que nada, el modulo de thetvdb se encuentra en 
/bots/liberclass/thetvdb/

Para empezar a trabajar debes primero instalar las liberclass:

cd liberclass
sudo python setup.py install

Luego debes ir a /bots/libercopy/ y ejecutar ./crawl para ver lo que te pueda gustar ;) 

Usage: crawl dialog              - Get, dowload site, put, view Log - the friendly way
Usage: crawl download [SITE]     - Download all site
Usage: crawl count [SITE]         - Count crawled items for site
Usage: crawl get [SITE] [LETTER] - Get site and letter using Scrapy
Usage: crawl put [SITE] [LETTER] - Put site and letter on LiberCopy
Usage: crawl help                - Shows this message
Usage: crawl log [SITE] [LETTER] - View logs for site and letter
Usage: crawl version             - Shows version

Las arañas se encuentran en
/bots/libercopy/liberbot/spiders

Los episodios que se van a crawlear se encuentran en 
/bots/libercopy/sites/SITIO/showlist

Los logs de los sitios que se crawlearon se encuentran en 
/bots/libercopy/sites/SITIO/debug

Los dumps json de los sitios crawleados se encuentra en 
/bots/libercopy/sites/SITIO/dump

NOTA: A fecha del 16/10/2010, los spiders funcionales son serie-online, eztv y series-danko
