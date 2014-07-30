# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blasstrap.models import Parallax, ParallaxContent, ParallaxImage


class ParallaxPlugin(CMSPluginBase):
    name = _('Parallax')
    module = _('Parallax')

    model = Parallax
    allow_children = True
    child_classes = ['ParallaxContentPlugin', 'ParallaxImagePlugin']

    render_template = 'plugins/parallax.html'


class ParallaxContentPlugin(CMSPluginBase):
    name = _('Content')
    module = _('Parallax')

    model = ParallaxContent
    require_parent = True
    parent_classes = ['ParallaxPlugin']

    render_template = 'plugins/parallax_content.html'


class ParallaxImagePlugin(CMSPluginBase):
    name = _('Image')
    module = _('Parallax')

    model = ParallaxImage
    require_parent = True
    parent_classes = ['ParallaxPlugin']

    render_template = 'plugins/parallax_image.html'

plugin_pool.register_plugin(ParallaxPlugin)
plugin_pool.register_plugin(ParallaxContentPlugin)
plugin_pool.register_plugin(ParallaxImagePlugin)


settings.CMS_PLACEHOLDER_CONF['parallax-content'] = {
    'name': _(u'Parallax content'),
    'default_plugins': [
        {
            'plugin_type': 'TextPlugin',
            'values': {
                'body': u"""
                    <h1>Parallax. <small>Sexigt.</small></h1><p>Innehållet i en parallax kan bestå av det mesta,
                    men håll dig till vanliga <code>h1</code> osv. samt <code>p</code> i textväg.</p>
                """
            },
        },
    ]
}
