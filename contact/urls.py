from django.conf.urls import patterns, include, url
from contact.views import ContactFormView

urlpatterns = patterns(
    '',
    url(r'^$', ContactFormView.as_view(success_url="/")),
)