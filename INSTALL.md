Entorno de desarrollo:
=======================

Instalacion del entorno de Desarrollo
-------------------------------------

Ejecutar install.sh en este mismo directorio:

`./install.sh`

Iniciando entorno de desarrollo
-------------------------------

`source virtual/bin/activate`

Importar datos de pruebas
-------------------------

`python manage.py loaddata apps/serie/fixtures/twin_peaks.json`

`cp -rp apps/serie/fixtures/img/* static/img/`

Salir del entorno de desarrollo
-------------------------------

`deactivate`


Indice de Búsquedas
-------------------

Si se importan datos hay que actualizar el indice de busquedas:

`python manage.py update_index`


Django-Rosetta
-------------------

Por un bug con los tests:

https://code.google.com/p/django-rosetta/issues/detail?id=107

`patch virtual/lib/python*/site-packages/django_rosetta*/rosetta/tests/__init__.py < src/rosetta.patch`


import-bot-data
-------------------

Para usar este comando hace falta instalar las siguientes dependencias

`pip install formencode`

`pip install IMDbPY`

`pip install tvdb_api simplejson`


DEFAULT_USER_FOR_LINKS
-------------------

Para que funcione la APP es necesario que exista un usuario configurado en el settings.py en la variable
DEFAULT_USER_FOR_LINKS. Este usuario es el que tendrá los links sin usuario.

