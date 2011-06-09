#!/bin/sh
# Script de instalacion para Ubuntu, en otras plataformas hay que cambiar el 
#  aptitude y los paquetes correspondientes

# Instalacion de dependencias
sudo aptitude install python-setuptools python-dev libxml2 libxslt1-dev libjpeg8-dev subversion && 
sudo easy_install -U pip &&

# Desde el directorio raiz (donde se encuentra README.txt)
# Preparamos el entorno virtual de desarrollo (como si fuera una jaula)
[ -d virtual ] || sudo pip install -U virtualenv virtualenvwrapper &&
[ -d virtual ] || pip -E virtual install django ipython PIL &&

# Con esto entramos a la jaula, vamos a tener que hacerlo siempre para entrar
. virtual/bin/activate &&

# Instalamos las dependencias
python setup.py develop && 

# La version del pip es antigua y da warnings
pip install src/django-registration-0.8-alpha-1.tar.gz && 

# Utilizamos el fork que acepta paginacion
# https://bitbucket.org/joeb/django-piston/
pip install src/django-piston-0.2.3rc1.tar.gz &&

# Utilizamos el fork de Kronuz que esta mas cuidado 
# Arregla este bug https://github.com/dcramer/django-ratings/issues/12
pip install src/django-ratings-0.3.6.tar.gz &&

# Herramientas de debugging
pip install ipdb django-debug-toolbar &&

# Desde petateca (donde esta manage.py)
cd petateca &&

# Creamos la DDBB y
python manage.py syncdb --noinput &&

# Hacemos las migraciones del South
python manage.py migrate &&  

# Creamos un usuario liberateca para las importaciones del bot y los datos de ejemplo, va a ser el User.id = 1 
python manage.py createsuperuser --noinput --username=liberateca --email=liberateca@liberateca.net &&

# Actualizamos campos de traduccion
python manage.py update_translation_fields &&

# Creamos el admin
python manage.py createsuperuser &&

# Iniciamos el servidor de desarrollo
python manage.py runserver
