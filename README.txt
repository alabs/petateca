Develop instalation
===================

# Instalacion de dependencias
    sudo aptitude install python-setuptools python-dev
    sudo easy_install -U pip
# Desde el directorio raiz
    sudo pip install -U virtualenv
    sudo pip install -U virtualenvwrapper
    pip -E virtual install django
    pip -E virtual install ipython
    source virtual/bin/activate
    python setup.py develop
# Desde liberweb (donde esta manage.py)    
# Con el --migrate ya no hace falta hacer los otros migrates
# FIXME: Falla con sqlite3
    python manage.py syncdb --migrate
    python manage.py runserver
    python manage.py update_translation_fields
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


Crawling framework 
==================

la documentacion se encuentra en 

liberweb/bots/README.txt


