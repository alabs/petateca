import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SITE_NAME = 'LiberCopy'

DEBUG = True
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
        'NAME': 'liberweb.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
#    'imdb': {
#        'ENGINE': 'postgresql_psycopg2',
#        'NAME': 'imdb',
#        'USER': 'libercopy',
#        'PASSWORD': 'libre',
#    },
}

TIME_ZONE = 'Europe/Madrid'

LANGUAGE_CODE = 'es'
ugettext = lambda s: s
LANGUAGES = (
 ('es', ugettext('Spanish')),
 ('en', ugettext('English')),
)
TRANSLATION_REGISTRY = 'translation'
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
)

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'invitation.middleware.LoginRequiredMiddleware',
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
    'context_processors.site_name',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'blog/fixtures')
)

INSTALLED_APPS = (
    'localeurl',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'serie',
    'blog',
    'userdata',
    #'imdblocal', #Don't use yet, sucks a lot
    'south',
    'modeltranslation',
    'rosetta',
    'sorl.thumbnail',
    'haystack',
    'djangoratings',
    'voting',
    'registration',
    'taggit',
    'django.contrib.comments',
    'avatar',
    'invitation',
)

DATABASE_ROUTERS = ['imdblocal.dbrouter.ImdbRouter']

#Valid values are http, sql
IMDB_ACCESS_SYSTEM = "http"  # XXX: sql search is worse

#uri for use with sql
IMDB_ACCESS_DB_URI = "postgres://liberweb:libre@localhost/imdb"

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

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'indexes')

# Registration
AUTH_PROFILE_MODULE = 'userdata.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = 'noreply@libercopy.net'

AUTHENTICATION_BACKENDS = (
    'userdata.models.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

FORCE_LOWERCASE_TAGS = True

try:
    from local_settings import *
except ImportError:
    pass

# Invitations
# Si se pone como True, redirige a /accounts/signin
INVITE_MODE = False
ACCOUNT_INVITATION_DAYS = 7
INVITATIONS_PER_USER = 5

LOGIN_EXEMPT_URLS = (
    r'^static/', 
)

LOGIN_URL_INDEX = '/accounts/signin/'
INVITATION_MAIL = 'invitaciones@libercopy.net'
ADMIN_MAIL = 'admin@libercopy.net'
