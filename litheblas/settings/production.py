# -*- coding: utf-8 -*-

from litheblas.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'dev.skorpan.lysator.liu.se',
    'litheblas.org',
    'www.litheblas.org'
]

#Till vilka adresser ska debug-epost skickas?
ADMINS = (
    ('Olle Vidner', 'olle@vidner.se'),
)

#Från vilken adress ska debug-epost skickas?
SERVER_EMAIL = 'django@' + getfqdn()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'litheblas',
        'USER': 'litheblas',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
    }
}
INSTALLED_APPS += ('blasbassync',)
STATIC_ROOT = os.path.join('/opt/litheblas.org/static')
MEDIA_ROOT = os.path.join('/opt/litheblas.org/media')


# MUST BE LAST IN FILE
try:
    from litheblas.settings.local import *
except ImportError:
    pass
# MUST BE LAST IN FILE