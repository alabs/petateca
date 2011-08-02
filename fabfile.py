#!/usr/bin/python

from fabric.api import run, env
from fabric.operations import abort
 
def prod():
    env.user = 'liberateca'
    env.hosts = [ 'liberateca.net' ]

 
# define needed functions here.
def test():
    result = run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && cd petateca && python manage.py test serie')
    if result.failed:
        abort('Fallo en el test de serie')
    result = run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && cd petateca && python manage.py test api')
    if result.failed:
        abort('Fallo en el test de API')

 
def deploy():
    #test()
    run('cd /srv/liberweb/liberweb/ && git pull alabs master')
    run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && python setup.py develop')
    run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && cd petateca && python manage.py syncdb --migrate')
#    update_index()
    run('sudo service uwsgi restart')

def sendinvitations():
    run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && cd petateca/ && python manage.py sendinvitations')

def update_index():
    run('cd /srv/liberweb/liberweb/ && source virtual/bin/activate && cd petateca/ && python manage.py update_index')

