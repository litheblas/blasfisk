# -*- coding: utf-8 -*-

from litheblas.settings import *

DEBUG = False
TEMPLATE_DEBUG = True

CRISPY_FAIL_SILENTLY = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'd*dvb_n#28xx9ij*f(-5=*9k9s57_=#!rqgrjl!2$&+b=%ujr$'
DATABASE_PASSWORD = None

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CMS_CACHE_DURATIONS = {
    'content': 0,
    'menus': 0,
    'permissions': 0
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'litheblas', 'media')


# MUST BE LAST IN FILE
try:
    from litheblas.settings.local import *
except ImportError:
    pass
# MUST BE LAST IN FILE__author__ = 'Kristoffer'
