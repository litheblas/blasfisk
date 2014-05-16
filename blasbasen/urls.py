from django.conf.urls import patterns, include, url
from blasbasen.views import PersonList

urlpatterns = patterns('',
    #url(r'^$', 'blasbasen.views.index'),
    url(r'^person/$', PersonList.as_view()),
    url(r'^person/(?P<person>\d+)/$', 'blasbasen.views.person_detail'),
    #url(r'^person/(?P<user>\d+)/edit/$', 'blasbasen.views.person_edit'),
    #url(r'^person/(?P<user>\d+)/delete/$', 'blasbasen.views.person_delete'),
    
    #url(r'section/$', 'blasbasen.views.section_list'),
    #url(r'section/(?P<section>)/$', 'blasbasen.views.section_detail'),
    
)