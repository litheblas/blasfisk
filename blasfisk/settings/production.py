# -*- coding: utf-8 -*-

from blasfisk.settings import *

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

INSTALLED_APPS += ('blasbassync',)
STATIC_ROOT = '/var/www/blasfisk/static'
MEDIA_ROOT = '/var/www/blasfisk/media'


# MUST BE LAST IN FILE
try:
    from blasfisk.settings.local import *
except ImportError:
    pass
# MUST BE LAST IN FILE