
* liberbot: 
    AKA 'BotsArmy'
** item.py: 
    Items de Scrapy (no hace falta tocarlo en principio)
** settings.py: 
    Configuraciones de los bots (cache, User Agent, etc)
** spiders/: 
    Spiders/bots. Ver A-template.py para crear algun sitio nuevo. 

* liberclass: 
    Diferentes librerias especificas de LiberCopy.
    AskLetter, FileExtract...

* scrapy.cfg / scrapy.db: 
    Configs de Scrapy
    scrapy crawl serie-online --set LETTER=B

* sites: 
    Cada sitio debe tener una carpeta creada (llamada igual que la variable name del spider), dentro de cada carpeta deben estar: 
** debug: 
    Logging
** dump: 
    El dump en formato Picle (.pkl)  
** showlist: 
    Listado de una por linea con las series que se quieren importar
