import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

# Hay algunas partes en las que no se puede cambiar, 
# asi que si se va a cambiar es recomendable hacer antes un
# egrep -R "(petateca|liberateca)" * 
SITE_NAME = 'Liberateca'

DEBUG = True
SENTRY_TESTING = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql',
        # 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': 'petateca.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

TIME_ZONE = 'Europe/Madrid'

LANGUAGE_CODE = 'es'
ugettext = lambda s: s
LANGUAGES = (
 ('es', ugettext('Spanish')),
 ('en', ugettext('English')),
)
#LOCALEURL_USE_ACCEPT_LANGUAGE = True
TRANSLATION_REGISTRY = 'core.translation'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static') 
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'd#1!3m895ycit%a9pflu%8cmg5llo&0ovnl(_2+h^0qsrn=d0&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sentry.client.middleware.Sentry404CatchMiddleware',
)


ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.site_name',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.markup',
    # django-app
    'registration', # users
# DEPRECATED    'invitation', # users
    'avatar', # users
    'south', # migrations
    'modeltranslation', # translations
    'rosetta', # translations
    'sorl.thumbnail', # thumbnails
    'haystack', # search
    'djangoratings', # ratings
    'voting', # ratings
    'piston', # API
    # customs
    'serie',
    'userdata',
    'api_v1',
    'api_v2',
    'search',
    'core',
    # sentry logger
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
)


THUMBNAIL_DEBUG = True
THUMBNAIL_SUBDIR = 'thumbs'

if DEBUG:
    try:
        #Check if django-debug-toolbar is installed
        import debug_toolbar
        MIDDLEWARE_CLASSES += (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

        INTERNAL_IPS = ('127.0.0.1',) 

        INSTALLED_APPS += ('debug_toolbar', ) 

        DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False} 
    except: 
        pass 

HAYSTACK_SITECONF = 'search.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'apps/search/indexes')

# Registration
AUTH_PROFILE_MODULE = 'userdata.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 15
LOGIN_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = 'noreply@liberateca.net'

AUTHENTICATION_BACKENDS = (
    'userdata.models.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

FORCE_LOWERCASE_TAGS = True


# Invitations
# Si se pone como True, redirige a /accounts/signin
# y permite el registro solo a traves de invitaciones de otros usuarios
# DEPRECTAED INVITE_MODE = True
INVITE_MODE = False
ACCOUNT_INVITATION_DAYS = 30 
INVITATIONS_PER_USER = 6
USER_WHO_INVITES = 'liberateca'
DEFAULT_USER_FOR_LINKS = 'liberateca'


LOGIN_EXEMPT_URLS = (
    r'^static/', 
    r'^accounts/invitation/request/$', 
    r'^admin/',
    r'^accounts/register/',
    r'^accounts/login/',
    r'^accounts/activate/',
    r'^accounts/password/reset/',
    # la API se encarga de la autenticacion
    # usuarios no registrados pueden entrar a la Doc
    r'^api/',
)

LOGIN_URL_INDEX = '/accounts/signin/'
INVITATION_MAIL = 'invitaciones@liberateca.net'
ADMIN_MAIL = 'admin@liberateca.net'


#CACHE_BACKEND = 'dummy://'

USE_ETAGS = True

SECURE_REQUIRED_PATHS = (
    '/admin/',
    '/accounts/',
)

#Valid values are http, sql
IMDB_ACCESS_SYSTEM = "http"  # XXX: sql search is worse

# Con local_settings podemos reescribir / agregar settings que sean 
# propios de la maquina donde se encuentre, por ejemplo BBDD y DEBUG
# MANTENER SIEMPRE ABAJO; PARA SOBREESCRIBIR

try:
    from local_settings import *
except ImportError:
    pass

if INVITE_MODE:
    MIDDLEWARE_CLASSES += (
        'userdata.middleware.LoginRequiredMiddleware',
    )

