from django.conf.urls import patterns, include, url
from blasbase.views import PersonList, PersonDetail, PersonAdd, PersonChange, SectionList

urlpatterns = patterns(
    '',
    #url(r'^$', 'blasbase.views.index'),
    url(r'^person/$', PersonList.as_view()),
    url(r'^person/add/$', PersonAdd.as_view(template_name_suffix='_add')),
    url(r'^person/(?P<pk>\d+)/$', PersonDetail.as_view(), name='person_detail'),
    url(r'^person/(?P<pk>\d+)/change/$', PersonChange.as_view(template_name_suffix='_change')),
    url(r'^section/$', SectionList.as_view()),
    #url(r'^person/(?P<user>\d+)/edit/$', 'blasbase.views.person_edit'),
    #url(r'^person/(?P<user>\d+)/delete/$', 'blasbase.views.person_delete'),
    
    #url(r'section/$', 'blasbase.views.section_list'),
    #url(r'section/(?P<section>)/$', 'blasbase.views.section_detail'),
    
)