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
    python manage.py convert_to_south serie #ver http://south.aeracode.org/docs/convertinganapp.html#converting-an-app
    python manage.py runserver
    python manage.py loaddata serie/fixtures/test_data.json

