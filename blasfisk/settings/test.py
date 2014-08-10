# -*- coding: utf-8 -*-

from blasfisk.settings.dev import *

DEBUG = True
TEMPLATE_DEBUG = True

CRISPY_FAIL_SILENTLY = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}