#!/bin/sh

# Instalacion de dependencias
sudo aptitude install python-setuptools python-dev
sudo easy_install -U pip

# Desde el directorio raiz (donde se encuentra README.txt)
# Preparamos el entorno virtual de desarrollo (como si fuera una jaula)
sudo pip install -U virtualenv virtualenvwrapper
pip -E virtual install django ipython PIL

# Con esto entramos a la jaula, vamos a tener que hacerlo siempre para entrar
source virtual/bin/activate

# Instalamos las dependencias
python setup.py develop

# Desde liberweb (donde esta manage.py)
cd liberweb

# Creamos la DDBB y hacemos las migraciones del South
python manage.py syncdb --migrate

# Actualizamos campos de traduccion
python manage.py update_translation_fields

# Datos de pruebas del blog
# Los contenidos se autoimportan por estar en el fichero liberweb/blog/fixtures/initial_data.json
cp -rp blog/fixtures/static/img/blog/blog/ static/img/

# Iniciamos el servidor de desarrollo
python manage.py runserver
