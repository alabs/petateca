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

NOTA: A fecha del 20/10/2010, los spiders funcionales son serie-online, cinetube, series-pepito, eztv y series-danko

$ ./crawl countall
[crawl] - Total Items crawled for all sites ==> 479445

---------

De liberclass una clase muy interesante es liberimport. La forma correcta de ejecutarla es a traves del manage.py en Django:

$ python manage.py shell

>>> from liberclass import liberimport
>>> help liberimport

LiberImport tiene las siguientes clases:
        CreateActor
        CreateEpisode
        CreateGenre
        CreateLanguage
        CreateLink
        CreateNetwork
        CreateSerie
        Import

Casi todas se ejecutan asi:

>>> a = liberimport.CreateActor('Frank Sinatra')
>>> a = a.create_actor()

a nos devuelve el objeto de Django: 

>>> a
>>> <Actor: Frank Sinatra>

Para cargar datos del scrapy, la forma mas facil es con Import:

>>> site='eztv'
>>> letter='F'
>>> 
>>> i = liberimport.Import()
>>> i.json_file('bots/libercopy/sites/' + site + '/dump/' + letter + '.json')

Para mas ejemplos ver el propio fichero de liberimport.py en liberclass/liberclass/liberimport.py


