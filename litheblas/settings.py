# -*- coding: utf-8 -*-

"""
Django settings for litheblas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

gettext = lambda s: s

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from litheblas.secret import SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost']

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'mydatabase',
#        'USER': 'mydatabaseuser',
#        'PASSWORD': 'mypassword',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Application definition

INSTALLED_APPS = (
    #CMS-specifikt
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
    
    #Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    #CMS-specifikt
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    #'djangocms_style',
    #'djangocms_column',
    #'djangocms_file',
    #'djangocms_flash',
    #'djangocms_googlemap',
    #'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    #'djangocms_teaser',
    #'djangocms_video',
    'reversion',
    
    #LiTHe Blås
    #'mailing',
    'blasbasen',
    #'events',
    #'watcher',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #CMS-specifikt
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
)


TEMPLATE_CONTEXT_PROCESSORS = (
    #CMS-specifikt
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static'
)

ROOT_URLCONF = 'litheblas.urls'

WSGI_APPLICATION = 'litheblas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'blasbasen.backends.BlasBackend',
)

AUTH_USER_MODEL = 'blasbasen.User'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'sv'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'litheblas', 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'litheblas', 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'litheblas', 'templates'),
)

#CMS-specifikt
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

SITE_ID = 1

LANGUAGES = (
    ('sv', _('Swedish')),
    ('en', _('English')),
    ('de', _('German')),
)

CMS_LANGUAGES = {
    'default': {
        'hide_untranslated': True,
        'redirect_on_fallback': True,
        'public': True,
        'fallbacks': ['sv'],
    },
    1: [
        {
            'code': 'sv',
            'name': _('Swedish'),
            'hide_untranslated': False,
            'public': True,
        },
        {
            'code': 'en',
            'name': _('English'),
            'public': True,
            'fallbacks': ['sv']
        },
        {
            'code': 'de',
            'name': _('German'),
            'public': True,
            'fallbacks': ['en', 'sv']
        },
    ],
}

CMS_TEMPLATES = (
    ('pages/page.html', _('Page')),
    ('pages/special_page.html', _('Special Page')),
    ('pages/feature.html', _('Page with Feature')),
    ('pages/home.html', _('LiTHe Hem')),
)

CMS_TEMPLATE_INHERITANCE = False #Annars ärver en massa sidor hem-mallen, vilken egentligen bara ska finnas på startsidan

CMS_PERMISSION = False

#Definierar några placeholders med standardinnehåll, typ vanliga sidor som bara behöver ha en text-plugin.
CMS_PLACEHOLDER_CONF = {
    'page-content': {
        'name': _(u'Page content'),
        'default_plugins':[
            {
                'plugin_type': 'TextPlugin',
                'values':{
                    'body': u'<p>Denna sida är tom. :(</p>'
                },
            },
        ]
    },
    'subtitle': {
        'name': _(u'Subtitle'),
        'plugins': ['TextPlugin'],
        'default_plugins':[
            {
                'plugin_type': 'TextPlugin',
                'values':{
                    'body': u''
                },
            },
        ],
    },
}

CKEDITOR_SETTINGS = {
    'language': 'en',
    'toolbar': 'CMS',
    'skin': 'moono',
    'allowedContent': 'false', #Stänger av filtrering av taggar.
}
