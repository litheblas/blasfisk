# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from blasstrap.models import Pusher, PusherEntry


class PusherEntryInline(StackedInline):
    model = PusherEntry
    extra = 3


class PusherPlugin(CMSPluginBase):
    name = _(u'Pusher')
    module = _(u'Bootstrap')

    model = Pusher
    allow_children = False
    render_template = "plugins/pusher.html"

    inlines = [PusherEntryInline]


plugin_pool.register_plugin(PusherPlugin)


settings.CMS_PLACEHOLDER_CONF['pusher-content'] = {
    'name': _(u'Jumbotron content'),
    'default_plugins': [
        {
            'plugin_type': 'TextPlugin',
            'values': {
                'body': u"""
                    <p>&nbsp;&nbsp;&nbsp;</p>
                """
            },
        },
    ]
}