# -*- coding: utf-8 -*-
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blasstrap.models import Container, Tagline


class ContainerPlugin(CMSPluginBase):
    name = _(u'Container')
    module = _(u'Bootstrap')

    model = Container
    allow_children = True
    render_template = "plugins/container.html"


class TaglinePlugin(CMSPluginBase):
    name = _(u'Tagline')
    module = _(u'Bootstrap')

    model = Tagline
    allow_children = False
    render_template = "plugins/tagline.html"

plugin_pool.register_plugin(ContainerPlugin)
plugin_pool.register_plugin(TaglinePlugin)

settings.CMS_PLACEHOLDER_CONF['tagline'] = {
    'name': _(u'Tagline'),
    'default_plugins': [
        {
            'plugin_type': 'MarkdownPlugin',
            'values': {
                'body': _(u'Write your tagline here.')
            },
        },
    ]
}