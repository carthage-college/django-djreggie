"""
Django settings for djreggie project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Debug
#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS

SECRET_KEY = 'ko53qfwb5(c23#ql62ru^n*3rr_@k%+x1-)v*d&6+bpsvh7b2!'
ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

SERVER_URL = "www.carthage.edu"
API_URL = "%s/%s" % (SERVER_URL, "api")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(__file__)
ROOT_URL = "/jsawyer/djreggie/"
ROOT_URLCONF = 'djreggie.urls'
WSGI_APPLICATION = 'djreggie.wsgi.application'
MEDIA_ROOT = 'home/jsawyer/sandbox/uploads/'
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = ''
STATIC_URL = "/static/"
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'djreggie',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'brahman',
        'PASSWORD': 'atm@n!@ke5ided3ri5i0n'
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.formtools',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'djtools',
    'djreggie.changemajor',
    'djreggie.consentfam',
    'djreggie.consentform',
    'djreggie.createemail',
    'djreggie.depstudent',
    'djreggie.indepstudent',
    'djreggie.systemaccess',
    'djreggie.undergradcandidacy',
)
LIVEWHALE_API_URL = "https://www.carthage.edu"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# template stuff
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    "/home/jsawyer/sandbox/djreggie/templates/",
    "/data2/django_templates/djkorra/",
    "/data2/django_templates/djcher/",
    "/data2/django_templates/",
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "djtools.context_processors.sitevars",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
)

# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/django_directory_cache',
        #'TIMEOUT': 60*20,
        #'KEY_PREFIX': "DIRECTORY_",
        #'OPTIONS': {
        #    'MAX_ENTRIES': 80000,
        #}
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = '636'
LDAP_PROTOCOL = "ldaps"
LDAP_BASE = ""
LDAP_USER = ""
LDAP_PASS = ""
LDAP_EMAIL_DOMAIN = ""
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/djreggie/accounts/login/'
LOGIN_REDIRECT_URL = '/djreggie/'
USE_X_FORWARDED_HOST = True
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN=".carthage.edu"
SESSION_COOKIE_NAME ='django_carthage_cookie'
SESSION_COOKIE_AGE = 86400

# logging
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'mugshots.upload': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'core': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
