# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ContactApp(CMSApp):
    name = _(u'Contact')
    urls = ['contact.urls']
    app_name = 'contact'  # Viktigt! Behövs för att kunna slå upp URL:er baklänges


apphook_pool.register(ContactApp)