# -*- coding: utf-8 -*-

# Utvecklingsspecfika inställningar

from litheblas.settings import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += ('debug_toolbar',)

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