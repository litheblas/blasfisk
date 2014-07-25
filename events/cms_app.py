# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class EventsApp(CMSApp):
    name = _(u'Events')
    urls = ['events.urls']
    app_name = 'events'  # Viktigt! Behövs för att kunna slå upp URL:er baklänges


apphook_pool.register(EventsApp)