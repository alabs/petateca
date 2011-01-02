Instalacion del entorno de Desarrollo
===================

Ejecutar install.sh en este mismo directorio:

./install.sh

Iniciando entorno de desarrollo
===================

source virtual/bin/activate

Import_bot_data
===================

Para importar los jsonses crawleados por scrapy: (Cambiar el sitio (eztv) y la letra (W.json))

python manage.py import_bot_data bots/libercopy/sites/eztv/dump/W.json 

Indice de Busquedas
==================

Si se importan datos hay que actualizar el indice de busquedas:

python manage.py update_index

Crawling framework 
==================

la documentacion se encuentra en 

liberweb/bots/README.txt
