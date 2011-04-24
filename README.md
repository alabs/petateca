PetaTeca: Bibliotecas públicas mantenidas por comunidades
=========================================================

PetaTeca es un proyecto basado en un simple concepto: La capacidad de autogestión colectiva de enlaces a recursos que deseen mantener las comunidades.

Tras esta sencilla idea, encontramos un proyecto que pretende ofrecer una herramienta de Software Libre a quienes deseen dotarse de una aplicación web que les permita mantener de manera colectiva enlaces a los contenidos que gestionen (como bibliotecas, asociaciones o cualquier tipo de institución) o también a comunidades y colectivos que deseen mantener un espacio común donde compartir enlaces a cualquier tipo de información de manera que los mismos puedan ser validados por ellas mismas.

PetaTeca es el software que mantiene a Liberateca ( http://liberateca.net/ ), donde se pueden compartir gustos y recomendaciones de series, aunque en un futuro soportara tambien libros, peliculas, musica y otras cosas. Para comentar nuevas funcionalidades a agregar en Liberateca, se puede hacer a traves del foro en UserVoice ( http://liberateca.uservoice.com/ )

Instalacion del entorno de Desarrollo
-------------------------------------

Ejecutar install.sh en este mismo directorio:

  ./install.sh

Iniciando entorno de desarrollo
-------------------------------

  source virtual/bin/activate

Importar datos de pruebas
-------------------------

  python manage.py loaddata apps/serie/fixtures/test_data.json 

  cp -rp apps/serie/fixtures/img/* static/img/

Salir del entorno de desarrollo
-------------------------------

  deactivate

Indice de Búsquedas
-------------------

Si se importan datos hay que actualizar el indice de busquedas:

  python manage.py update_index


Compresion de CSS/JS
-------------------

Para optimizar las consultas HTTP, se comprimen con django-compress. Para iniciar la compresion o si realizas algun cambio en el CSS/JS, tienes que regenerar el fichero comprimido

  python manage.py synccompress


Django-Invitation
-------------------

Al no tener migraciones, se tuvo que copiar la app al directorio petateca/apps/invitation


Django-Rosetta
-------------------

Por un bug con los tests:
https://code.google.com/p/django-rosetta/issues/detail?id=107

  patch virtual/lib/python*/site-packages/django_rosetta*/rosetta/tests/__init__.py < src/rosetta.patch 
