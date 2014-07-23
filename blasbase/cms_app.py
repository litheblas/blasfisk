# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BlasbaseApp(CMSApp):
    name = _(u'Blåsbase')
    urls = ['blasbase.urls']
    app_name = 'blasbase'  # Viktigt! Behövs för att kunna slå upp URL:er baklänges


apphook_pool.register(BlasbaseApp)