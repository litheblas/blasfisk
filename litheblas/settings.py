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
SECRET_KEY = 'd*dvb_n#28xx9ij*f(-5=*9k9s57_=#!rqgrjl!2$&+b=%ujr$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #CMS-specifikt
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
    
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
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'reversion',
    
    #LiTHe Blås
    'mailing',
    'blasbasen',
    'events',
    'watcher',
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
    'cms.context_processors.media',
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

LANGUAGE_CODE = 'se'

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
    ## Customize this
    ('se', _('Swedish')),
    ('en', _('English')),
    ('de', _('German')),
)

CMS_LANGUAGES = {
    'default': {
        'hide_untranslated': True,
        'redirect_on_fallback': True,
        'public': True,
    },
    1: [
        {
            'code': 'se',
            'name': _('Swedish'),
            'hide_untranslated': False,
            'public': True,
        },
        {
            'code': 'en',
            'name': _('English'),
            'public': True,
        },
        {
            'code': 'de',
            'name': _('German'),
            'public': True,
            'fallbacks': ['en']
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('page.html', _('Page')),
    ('feature.html', _('Page with Feature'))
)

CMS_PERMISSION = False

CMS_PLACEHOLDER_CONF = {}
