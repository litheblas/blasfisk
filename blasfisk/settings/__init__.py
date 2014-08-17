# -*- coding: utf-8 -*-
"""
Django settings for blasfisk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _
from socket import getfqdn

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'blasfisk', 'static'),)

INSTALLED_APPS = (
    # CMS-specifikt
    'djangocms_admin_style',
    'djangocms_text_ckeditor',
    
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    # CMS-specifikt
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
    #'reversion',
    
    # Andra appar
    'imagekit',
    'django_filters',
    'crispy_forms',
    'djangocms_markdown',
    'markdown_deux',
    'djangocms_parallax',
    
    # LiTHe Blås
    'blasstrap',
    #'mailing',
    'blasbase',
    'cards',
    'events',
    'locations',
    #'watcher',
    'contact',
    'attendance',
)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

MARKDOWN_DEUX_STYLES = {
    'default': {
        'safe_mode': False,
        'extras': {
            # 'smarty-pants': True
        }
    }
}

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

ROOT_URLCONF = 'blasfisk.urls'

WSGI_APPLICATION = 'blasfisk.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'blasbase.backends.BlasbaseBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'blasbase.User'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'sv'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

#CMS-specifikt
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'blasfisk', 'templates'),
)

SITE_ID = 1

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'conf', 'locale'),
)

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
    ('pages/page.html', _('Page')),  # Först i listan, blir standard
    ('pages/base.html', _('Base Page')),
    ('pages/home.html', _('LiTHe Home')),
)

CMS_TEMPLATE_INHERITANCE = False  # Annars ärver en massa sidor hem-mallen, vilken egentligen bara ska finnas på startsidan

CMS_PERMISSION = False

# Definierar några placeholders med standardinnehåll, typ vanliga sidor som bara behöver ha en text-plugin.
CMS_PLACEHOLDER_CONF = {
    'page-content': {
        'name': _(u'Page content'),
        'default_plugins': [
            {
                'plugin_type': 'MarkdownPlugin',
                'values': {
                    'body': u'<p class="lead">Här skriver du eventuell ingress.</p>\n\nLorem ipsum dolor sit amet, **för helvete**.'
                },
            },
        ]
    },
    'parallax-content': {
        'name': _(u'Parallax content'),
        'default_plugins': [
            {
                'plugin_type': 'MarkdownPlugin',
                'values': {
                    'body': u'# Parallax. <small>Sexigt.</small>\nLorem ipsum dolor sit amet.\n\n<a href="" class="btn btn-primary">Bam!</a>'
                },
            },
        ]
    }
}

CKEDITOR_SETTINGS = {
    'language': 'sv',
    'toolbar': 'CMS',
    'skin': 'moono',
    
    # Ta bort ett gäng plugins och knappar
    'removePlugins': 'pastefromword,magicline,colordialog',  # Akta dig, inga mellanslag mellan namnen...
    'removeButtons': 'TextColor,BGColor,Indent,Outdent',  # Akta dig, inga mellanslag mellan namnen...
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CONTACT_SUBJECTS = (
    ('general', _('General questions')),
    ('concerts', _('Concerts')),
)

CONTACT_SUBJECT_RECIPIENTS = {
    # '<subject key>': ['recipient1@a.com', 'recipient2@b.com', ...]
    'general': ['lithe.blas@music.liu.se'],
    'concerts': ['spelraggare@litheblas.org'],
}

# Name of the default event type
# Used with a get_or_create, so shouldn't be translatable
DEFAULT_EVENT_TYPE = 'Spelning'