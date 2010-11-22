Develop instalation
===================

# Instalacion de dependencias
    sudo aptitude install python-setuptools python-dev
    sudo easy_install -U pip
# Desde el directorio raiz
    sudo pip install -U virtualenv virtualenvwrapper
    pip -E virtual install django ipython PIL
    source virtual/bin/activate
    python setup.py develop
# Desde liberweb (donde esta manage.py)
    python manage.py syncdb --migrate
    python manage.py update_translation_fields
    python manage.py runserver
# FIXME: Hay que agregar fixtures validos
#    python manage.py loaddata serie/fixtures/test_data.json

Updates
=======

2010-10-20
----------

desde el directorio liberweb (donde está manage.py)::

    python manage.py migrate serie 0001 --fake
    python manage.py migrate
    python manage.py update_translation_fields

2010-11-09
----------

# Para importar los jsonses crawleados por scrapy:
# Cambiar el sitio (eztv) y la letra (W.json)
    python manage.py import_bot_data bots/libercopy/sites/eztv/dump/W.json 


2010-11-11
----------

# Para que funcionen los thumbnails
    source virtual/bin/activate
    pip install sorl-thumbnail PIL

2010-11-22
----------


cp -rp blog/fixtures/static/img/blog/ static/img/blog/ 
# Si se hace un syncdb --migrate es automagico, no hace falta hacer el migrate ni el loaddata
python manage.py migrate blog 0001 --fake
python manage.py loaddata blog/fixtures/initial_data.json 

Crawling framework 
==================

la documentacion se encuentra en 

liberweb/bots/README.txt

