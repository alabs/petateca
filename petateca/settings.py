import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

# Hay algunas partes en las que no se puede cambiar, 
# asi que si se va a cambiar es recomendable hacer antes un
# egre -R "(petateca|liberateca)" * 
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
#    'imdb': {
#        'ENGINE': 'postgresql_psycopg2',
#        'NAME': 'imdb',
#        'USER': 'petateca',
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
LOCALEURL_USE_ACCEPT_LANGUAGE = True
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
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'userdata.middleware.LoginRequiredMiddleware',
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
    'context_processors.site_name',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'blog/fixtures')
)

INSTALLED_APPS = (
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
    'registration',
    'invitation',
    'south',
    'modeltranslation',
    'rosetta',
    'sorl.thumbnail',
    'haystack',
    'djangoratings',
    'voting',
    'taggit',
    'django.contrib.comments',
    'avatar',
    #Sentry
    # don't forget to add the dependencies!
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    'compress',
)

DATABASE_ROUTERS = ['imdblocal.dbrouter.ImdbRouter']

#Valid values are http, sql
IMDB_ACCESS_SYSTEM = "http"  # XXX: sql search is worse

#uri for use with sql
IMDB_ACCESS_DB_URI = "postgres://petateca:libre@localhost/imdb"

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
DEFAULT_FROM_EMAIL = 'noreply@liberateca.net'

AUTHENTICATION_BACKENDS = (
    'userdata.models.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

FORCE_LOWERCASE_TAGS = True


# Invitations
# Si se pone como True, redirige a /accounts/signin
# y permite el registro solo a traves de invitaciones de otros usuarios
INVITE_MODE = False
ACCOUNT_INVITATION_DAYS = 7
INVITATIONS_PER_USER = 6
USER_WHO_INVITES = 'liberateca'

LOGIN_EXEMPT_URLS = (
    r'^static/', 
    r'^accounts/invitation/request/$', 
    r'^accounts/invitation/thanks/$', 
    r'^admin/',
    r'^accounts/register/',
    r'^accounts/activate/',
)

LOGIN_URL_INDEX = '/accounts/signin/'
INVITATION_MAIL = 'invitaciones@liberateca.net'
ADMIN_MAIL = 'admin@liberateca.net'

# compress app settings
COMPRESS_CSS = {
    'all': {
        'source_filenames': (
            'css/reset.css',
            'css/styles.css',
            'css/jquery.colorbox.css',
            'css/jquery.jgrowl.css',
            'css/jquery.rating.css',
            'css/jquery.autocomplete.css',
            'css/jquery.bubblepopup.v2.3.1.css',
            'css/jquery.sorter_blue.css',
        ),
        'output_filename': 'css/compressed-?.css',
    },
}

COMPRESS_JS = {
    'all': {
        'source_filenames': (
            'js/jquery-min.js',
            'js/jquery.autocomplete.js',
            'js/jquery.colorbox.js',
            'js/jquery.dimensions.min.js',
            'js/jquery.easing.1.3.js',
            'js/jquery.jgrowl.js',
            'js/jquery.rating.js',
            'js/jquery.bubblepopup.v2.3.1.min.js',
            'js/petateca.js',
# Da un error de Undetermined Regular Expression     'js/jquery.tablesorter.js',
        ),
        'output_filename': 'js/compressed-?.js',
    },
}

COMPRESS = True
COMPRESS_VERSION = True

try:
    from local_settings import *
except ImportError:
    pass

