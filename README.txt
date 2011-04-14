PetaTeca: Bibliotecas públicas mantenidas por comunidades
===================

PetaTeca es un proyecto basado en un simple concepto: La capacidad de 
autogestión colectiva de enlaces a recursos que deseen mantener las 
comunidades.

Tras esta sencilla idea, encontramos un proyecto que pretende ofrecer una 
herramienta de Software Libre a quienes deseen dotarse de una aplicación web 
que les permita mantener de manera colectiva enlaces a los contenidos que 
gestionen (como bibliotecas, asociaciones o cualquier tipo de institución) 
o también a comunidades y colectivos que deseen mantener un espacio común 
donde compartir enlaces a cualquier tipo de información de manera que los 
mismos puedan ser validados por ellas mismas.

Instalacion del entorno de Desarrollo
===================
Ejecutar install.sh en este mismo directorio:
$ ./install.sh

Iniciando entorno de desarrollo
===================
$ source virtual/bin/activate

Importar datos de pruebas
===================
$ python manage.py loaddata serie/fixtures/test_data.json 
$ cp -rp serie/fixtures/img/* static/img/

Salir del entorno de desarrollo
===================
$ deactivate

Indice de Busquedas
==================
Si se importan datos hay que actualizar el indice de busquedas:
$ python manage.py update_index

Compresion de CSS/JS
==================
Para optimizar las consultas HTTP, se comprimen con django-compress
Para iniciar la compresion o si realizas algun cambio en el CSS/JS, tienes
que regenerar el ficheor comprimido
$ python manage.py synccompress
