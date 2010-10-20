Develop instalation
===================

desde el directorio raiz del proyecto::

    sudo aptitude install python-setuptools python-dev
    sudo easy_install -U pip
    sudo pip install -U virtualenv
    sudo pip install -U virtualenvwrapper
    pip -E virtual install django
    pip -E virtual install ipython
    source virtual/bin/activate
    python setup.py develop

desde el directorio liberweb (donde está manage.py):
    
    python manage.py syncdb
    python manage.py runserver
    python manage.py loaddata serie/fixtures/test_data.json

Crawling framework 
==================

la documentacion se encuentra en 

liberweb/bots/README.txt
