from django.conf.urls import patterns, include, url
from events.views import EventList

urlpatterns = patterns(
    '',
    url(r'^$', EventList.as_view()),
)