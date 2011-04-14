#!/bin/sh
# Script de instalacion para Ubuntu, en otras plataformas hay que cambiar el 
#  aptitude y los paquetes correspondientes

# Instalacion de dependencias
sudo aptitude install python-setuptools python-dev libxml2 libxslt1-dev libjpeg-dev subversion csstidy && 
sudo easy_install -U pip &&

# Desde el directorio raiz (donde se encuentra README.txt)
# Preparamos el entorno virtual de desarrollo (como si fuera una jaula)
sudo pip install -U virtualenv virtualenvwrapper &&
pip -E virtual install django==1.2.3 ipython PIL &&

# Con esto entramos a la jaula, vamos a tener que hacerlo siempre para entrar
. virtual/bin/activate &&

# Instalamos las dependencias
python setup.py develop && 

# Desde petateca (donde esta manage.py)
cd petateca &&

# Creamos la DDBB y hacemos las migraciones del South
python manage.py syncdb --migrate &&

# Actualizamos campos de traduccion
python manage.py update_translation_fields &&


# Iniciamos el servidor de desarrollo
python manage.py runserver
