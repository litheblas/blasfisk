# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from cms.sitemaps import CMSSitemap

from django.contrib import admin
admin.autodiscover()

# URL:er som hamnar under roten
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^login/$', 'django.contrib.auth.views.login'),

    url(r'^400/$', TemplateView.as_view(template_name='400.html')),  # Test för 400-sidan
    url(r'^403/$', TemplateView.as_view(template_name='403.html')),  # Test för 403-sidan
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),  # Test för 404-sidan
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),  # Test för 500-sidan
    url(r'^test/$', TemplateView.as_view(template_name='test.html')),
    
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

# URL:er som hamnar under respektive språkkod, typ /sv/
urlpatterns += i18n_patterns('',
    url(r'^', include('cms.urls')), # <--------- include the django cms urls via i18n_patterns
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
) + urlpatterns